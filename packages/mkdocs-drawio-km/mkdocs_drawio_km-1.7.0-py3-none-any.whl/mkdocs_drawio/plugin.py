import re, os
import json

import ssl
import tempfile
import urllib
import uuid
import mkdocs
import string
import logging
from lxml import etree
from typing import Dict
from html import escape
from pathlib import Path
from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin
import datetime

# ------------------------
# Constants and utilities
# ------------------------
REFRESH_URL_TEMPLATE = string.Template(
    '<a href="#" onclick="fetch(\'$refresh_url\')">刷新文档</a>'
)

SUB_TEMPLATE = string.Template(
    '<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="$config"></div>'
)

KITY_MINDER_TEMPLATE = string.Template(
    '<div id="$minder_view_id" type="application/kityminder" minder-data-type="json"></div>'
)

LOGGER = logging.getLogger("mkdocs.plugins.diagrams")


# ------------------------
# Plugin
# ------------------------
class DrawioPlugin(BasePlugin):
    """
    Plugin for embedding Drawio Diagrams into your MkDocs
    """

    config_scheme = (
        (
            "refresh_url",
            mkdocs.config.config_options.Type(str, default="https://de.vicp.net:58765"),
        ),
        (
            "kity_minder_toolbar",
            mkdocs.config.config_options.Type(
                str,
                default="<button id='btn-${minder_view_id}-zoom-in' class='btn-minder-view-toolbar'>➖</button><button id='btn-${minder_view_id}-zoom-out' class='btn-minder-view-toolbar'>➕</button><button id='btn-${minder_view_id}-full' class='btn-minder-view-toolbar'>&#9974;</button>",
            ),
        ),
        (
            "kity_minder_global_style",
            mkdocs.config.config_options.Type(
                str,
                default="""                                              
        .btn-minder-view-toolbar {
            border: 1px solid #dbb656;
            padding: 1px 5px;
            background-color: #fff2cc;
            cursor: pointer;
        }
""",
            ),
        ),
        (
            "kity_minder_container_style",
            mkdocs.config.config_options.Type(
                str,
                default="""
        #${minder_view_id}
        {                                                  
            border: 1px solid #ccc;
            left: 10px;
            top: 10px;
            bottom: 10px;
            right: 10px;
            height: ${alt_height};
            width: ${alt_width};
            overflow: auto;
        }
        #${minder_view_id} svg
        {                                               
            min-height: ${alt_height};
        }
""",
            ),
        ),
        (
            "kity_minder_container_javascript",
            mkdocs.config.config_options.Type(
                str,
                default="""                                              
        if(!kmLists) { var kmLists = []; }
        kmLists.push(new kityminder.Minder());
        kmLists[kmLists.length -1].renderTo(document.querySelector('#${minder_view_id}'));
        kmLists[kmLists.length -1].importJson(${file_content});
        if(!zoomContainer){
            var zoomContainer=function(container, scale){
                const cw = container.offsetWidth;
                const nw = cw * scale;
                container.style.width = nw + 'px';
                const ch = container.offsetHeight;
                const nh = ch * scale;
                container.style.height = nh + 'px';
                const svg = container.querySelector('svg')
                svg.style.minWidth = nw + 'px';
                svg.style.minHeight = nh + 'px';
            }
        }
        if(!fullContainer){
            var fullContainer=function(svgElement){
                if (svgElement) {
                    if (svgElement.requestFullscreen) {
                        svgElement.requestFullscreen();
                    } else if (svgElement.mozRequestFullScreen) {
                        svgElement.mozRequestFullScreen();
                    } else if (svgElement.webkitRequestFullscreen) {
                        svgElement.webkitRequestFullscreen();
                    } else if (svgElement.msRequestFullscreen) {
                        svgElement.msRequestFullscreen();
                    }
                }
            }
        }
        document.getElementById('btn-${minder_view_id}-zoom-in') && document.getElementById('btn-${minder_view_id}-zoom-in').addEventListener('click', function() {
            zoomContainer(document.getElementById('${minder_view_id}'), 0.8)
        });
        document.getElementById('btn-${minder_view_id}-zoom-out') && document.getElementById('btn-${minder_view_id}-zoom-out').addEventListener('click', function() {
            zoomContainer(document.getElementById('${minder_view_id}'), 1.2)
        });
        document.getElementById('btn-${minder_view_id}-full') && document.getElementById('btn-${minder_view_id}-full').addEventListener('click', function() {
            fullContainer(document.getElementById('${minder_view_id}').querySelector('svg'))
        });
        document.getElementById('${minder_view_id}') && document.getElementById('${minder_view_id}').addEventListener('dblclick', function() {
            const svg = this.querySelector('svg')
            const divBackground = window.getComputedStyle(this).background;
            if(!svg.hasFullscreenListener){
              svg.addEventListener("fullscreenchange", function() {
                  if (document.fullscreenElement) {
                      svg.style.background = divBackground;
                  } else {
                      svg.style.background = "";
                  }
              });
              svg.hasFullscreenListener = true
            }
            fullContainer(this.querySelector('svg'));
        });
""",
            ),
        ),
        (
            "viewer_js",
            mkdocs.config.config_options.Type(
                str, default="https://viewer.diagrams.net/js/viewer-static.min.js"
            ),
        ),
        (
            "kity_js",
            mkdocs.config.config_options.Type(
                str,
                default="https://cdn.jsdelivr.net/npm/kity@2.0.4/dist/kity.min.js",
            ),
        ),
        (
            "kityminder_core_js",
            mkdocs.config.config_options.Type(
                str,
                default="https://cdn.jsdelivr.net/npm/kityminder-core@1.4.50/dist/kityminder.core.min.js",
            ),
        ),
        (
            "kityminder_core_css",
            mkdocs.config.config_options.Type(
                str,
                default="https://cdn.jsdelivr.net/npm/kityminder-core@1.4.50/dist/kityminder.core.min.css",
            ),
        ),
        ("toolbar", mkdocs.config.config_options.Type(bool, default=True)),
        ("tooltips", mkdocs.config.config_options.Type(bool, default=True)),
        ("border", mkdocs.config.config_options.Type(int, default=0)),
    )

    def on_post_page(self, output_content, config, page, **kwargs):
        if (
            ".drawio" not in output_content.lower()
            and ".km" not in output_content.lower()
        ):
            return output_content
        now_str = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        LOGGER.error(f"{now_str} ------ on_post_page:: {page.file.abs_dest_path}")
        soup = BeautifulSoup(output_content, "html.parser")
        parser_executed = False
        # search for images using drawio extension
        km_diagrams = soup.findAll("img", src=re.compile(r".*\.km$", re.IGNORECASE))
        drawio_diagrams = soup.findAll(
            "img", src=re.compile(r".*\.drawio$", re.IGNORECASE)
        )
        if len(drawio_diagrams) > 0 and self.render_drawio_diagrams(
            page, soup, drawio_diagrams
        ):
            parser_executed = True
            now_str = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
            LOGGER.error(
                f"{now_str} ------ on_post_page:: render_drawio_diagrams {page.file.abs_dest_path}"
            )

        if len(km_diagrams) > 0 and self.render_km_diagrams(page, soup, km_diagrams):
            parser_executed = True
            now_str = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
            LOGGER.error(
                f"{now_str} ------ on_post_page:: render_km_diagrams {page.file.abs_dest_path}"
            )
        if parser_executed:
            return str(soup)
        else:
            return output_content

    def render_drawio_diagrams(self, page, soup: BeautifulSoup, diagrams):
        plugin_config = self.config.copy()

        diagram_config = {
            "toolbar": "zoom" if plugin_config["toolbar"] else None,
            "tooltips": "1" if plugin_config["tooltips"] else "0",
            "border": plugin_config["border"] + 5,
            "resize": "1",
            "edit": "_blank",
            "refresh_url": plugin_config["refresh_url"],
        }

        # search for images using drawio extension

        # add drawio library to body
        soup.body.append(soup.new_tag("script", src=plugin_config["viewer_js"]))

        # substitute images with embedded drawio diagram
        path = Path(page.file.abs_dest_path).parent

        for diagram in diagrams:
            if re.search("^https?://", diagram["src"]):
                # mxgraph = BeautifulSoup(
                #     DrawioPlugin.substitute_with_url(diagram_config, diagram["src"]),
                #     "html.parser",
                # )
                downloaded_file = DrawioPlugin.download_file(diagram["src"])
                mxgraph = BeautifulSoup(
                    DrawioPlugin.substitute_with_file(
                        diagram_config,
                        path,
                        downloaded_file,
                        diagram["alt"],
                    ),
                    "html.parser",
                )
                os.remove(downloaded_file)
            else:
                mxgraph = BeautifulSoup(
                    DrawioPlugin.substitute_with_file(
                        diagram_config, path, diagram["src"], diagram["alt"]
                    ),
                    "html.parser",
                )

            diagram.replace_with(mxgraph)

        return True

    def render_km_diagrams(self, page, soup: BeautifulSoup, diagrams):
        plugin_config = self.config.copy()
        # add drawio library to body
        soup.body.append(
            soup.new_tag(
                "link", rel="stylesheet", href=plugin_config["kityminder_core_css"]
            )
        )
        style_tag = soup.new_tag("style")
        style_tag["type"] = "text/css"

        # 在 <script> 标签内插入 JavaScript 代码
        style_tag.string = string.Template(
            plugin_config["kity_minder_global_style"]
        ).substitute()
        soup.body.append(style_tag)

        soup.body.append(
            soup.new_tag(
                "script",
                type="text/javascript",
                src=plugin_config["kity_js"],
            )
        )
        soup.body.append(
            soup.new_tag(
                "script",
                type="text/javascript",
                src=plugin_config["kityminder_core_js"],
            )
        )

        # substitute images with embedded drawio diagram
        path = Path(page.file.abs_dest_path).parent
        KITY_MINDER_CONTAINER_JS_TEMPLATE = string.Template(
            plugin_config["kity_minder_container_javascript"]
        )
        KITY_MINDER_CONTAINER_CSS_TEMPLATE = string.Template(
            plugin_config["kity_minder_container_style"]
        )
        refresh_url = plugin_config["refresh_url"]
        toolbar_template = plugin_config["kity_minder_toolbar"]
        for diagram in diagrams:
            minder_view_id = f"minder-view-{uuid.uuid4()}"
            diagram_alt = diagram["alt"] if diagram["alt"] else "400px,400px"

            if re.search("^https?://", diagram["src"]):
                downloaded_file = DrawioPlugin.download_file(diagram["src"])
                mxgraph, file_content = DrawioPlugin.substitute_km_with_file(
                    path,
                    downloaded_file,
                    diagram_alt,
                    minder_view_id,
                    refresh_url,
                    toolbar_template,
                )
                os.remove(downloaded_file)
            else:
                mxgraph, file_content = DrawioPlugin.substitute_km_with_file(
                    path,
                    diagram["src"],
                    diagram_alt,
                    minder_view_id,
                    refresh_url,
                    toolbar_template,
                )
            diagram.replace_with(BeautifulSoup(mxgraph, "html.parser"))
            script_tag = soup.new_tag("script")
            script_tag["type"] = "text/javascript"
            script_tag.string = KITY_MINDER_CONTAINER_JS_TEMPLATE.substitute(
                file_content=file_content, minder_view_id=minder_view_id
            )
            soup.body.append(script_tag)
            style_tag = soup.new_tag("style")
            style_tag["type"] = "text/css"
            diagram_alt_lists = diagram_alt.split(",")
            alt_height = diagram_alt_lists[0]
            alt_width = diagram_alt_lists[1] if len(diagram_alt_lists) > 1 else "600px"
            style_tag.string = KITY_MINDER_CONTAINER_CSS_TEMPLATE.substitute(
                minder_view_id=minder_view_id,
                alt=alt_height,
                alt_height=alt_height,
                alt_width=alt_width,
            )
            soup.body.append(style_tag)

        return True

    @staticmethod
    def substitute_with_url(config: Dict, url: str) -> str:
        config["url"] = url

        return SUB_TEMPLATE.substitute(config=escape(json.dumps(config)))

    @staticmethod
    def download_file(url):
        fd, path = tempfile.mkstemp()
        context = ssl._create_unverified_context()
        # 使用 urllib.request 下载文件
        with urllib.request.urlopen(url, context=context) as response:
            with open(path, "wb") as out_file:
                data = response.read()  # 读取响应内容
                out_file.write(data)  # 写入本地文件
        return path

    @staticmethod
    def substitute_with_file(config: Dict, path: Path, src: str, alt: str) -> str:
        try:
            fresh_url_content = ""
            if os.path.isabs(src):
                diagram_xml = etree.parse(Path(src))
                fresh_url_content = REFRESH_URL_TEMPLATE.substitute(
                    refresh_url=config["refresh_url"]
                )
            else:
                diagram_xml = etree.parse(path.joinpath(src).resolve())
        except Exception:
            LOGGER.error(
                f"Error: Provided diagram file '{src}' on path '{path}' is not a valid diagram"
            )
            diagram_xml = etree.fromstring("<invalid/>")

        diagram = DrawioPlugin.parse_diagram(diagram_xml, alt)
        config["xml"] = diagram

        return fresh_url_content + SUB_TEMPLATE.substitute(
            config=escape(json.dumps(config))
        )

    @staticmethod
    def substitute_km_with_file(
        path: Path,
        src: str,
        alt: str,
        minder_view_id: str,
        refresh_url: str,
        toolbar_template: str,
    ) -> str:
        file_content: str
        fresh_url_content = ""
        try:
            file_path: Path
            if os.path.isabs(src):
                file_path = Path(src)
                fresh_url_content = REFRESH_URL_TEMPLATE.substitute(
                    refresh_url=refresh_url
                )
            else:
                file_path = path.joinpath(src).resolve()
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
        except Exception:
            LOGGER.error(
                f"Error: Provided Kity Minder diagram file '{src}' on path '{path}' is not a valid diagram"
            )
        return (
            fresh_url_content
            + string.Template(toolbar_template).substitute(
                minder_view_id=minder_view_id
            )
            + KITY_MINDER_TEMPLATE.substitute(minder_view_id=minder_view_id),
            file_content,
        )

    @staticmethod
    def parse_diagram(data, alt, src="", path=None) -> str:
        if alt is None or len(alt) == 0:
            return etree.tostring(data, encoding=str)

        try:
            mxfile = data.xpath("//mxfile")[0]

            # try to parse for a specific page by using the alt attribute
            page = mxfile.xpath(f"//diagram[@name='{alt}']")

            if len(page) == 1:
                parser = etree.XMLParser()
                result = parser.makeelement(mxfile.tag, mxfile.attrib)

                result.append(page[0])
                return etree.tostring(result, encoding=str)
            else:
                LOGGER.warning(
                    f"Warning: Found {len(page)} results for page name '{alt}' for diagram '{src}' on path '{path}'"
                )

            return etree.tostring(mxfile, encoding=str)
        except Exception:
            LOGGER.error(
                f"Error: Could not properly parse page name '{alt}' for diagram '{src}' on path '{path}'"
            )
        return ""
