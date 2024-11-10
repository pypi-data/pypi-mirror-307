# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Nginx"
"""
  * @File    :   Nginx.py
  * @Time    :   2023/04/26 01:06:07
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""
import crossplane
from pathlib import Path

from xy_string.utils import is_empty_string
from xy_web_server.ModuleData import ModuleData


class Nginx:
    def location_quick_configure(
        self,
        url_path: str,
        upstream: str,
        pass_method: str = "proxy_pass",
        set_headers: list = [],
        includes: list = [],
        extension: dict = {},
    ) -> dict | None:
        configure: dict | None = self.location_full_configure(
            url_path=url_path,
            upstream=upstream,
            pass_method=pass_method,
            set_headers=set_headers,
            includes=includes,
            extension=extension,
        )
        if not isinstance(configure, dict):
            return None
        configure.setdefault("client_max_body_size", "1G")
        default_timeout = "9900s"
        configure.setdefault("proxy_send_timeout", default_timeout)
        configure.setdefault("proxy_read_timeout", default_timeout)
        configure.setdefault("proxy_connect_timeout", default_timeout)
        configure.setdefault("send_timeout", default_timeout)
        configure.setdefault("chunked_transfer_encoding", "on")
        configure.setdefault("proxy_http_version", "1.1")
        if isinstance(extension, dict):
            configure.update(extension)
        return configure

    def location_full_configure(
        self,
        url_path: str,
        upstream: str,
        pass_method: str = "proxy_pass",
        set_headers: list = [],
        includes: list = [],
        extension: dict = {},
    ) -> dict | None:
        if is_empty_string(url_path) or is_empty_string(upstream):
            return None
        if is_empty_string(pass_method):
            pass_method = "proxy_pass"
        configure = {}
        configure.setdefault("nginx_location_url_path", url_path)
        configure.setdefault("proxy_pass", upstream)
        configure.setdefault(
            "set_headers",
            "\n".join([f"proxy_set_header {header};" for header in set_headers]).join(
                "\n"
            ),
        )
        configure.setdefault(
            "includes",
            "\n".join([f"include {include};" for include in includes]).join("\n"),
        )
        if isinstance(extension, dict):
            configure.update(extension)
        return configure

    def location_string(self, configure: dict) -> str | None:
        if not configure or not isinstance(configure, dict):
            return None
        set_headers = configure.get("set_headers")
        if not is_empty_string(set_headers):
            del configure["set_headers"]
        includes = configure.get("includes")
        if not is_empty_string("includes"):
            del configure["includes"]
        url_path = configure.get("nginx_location_url_path")
        if not url_path:
            del configure["url_path"]
        format_map = {}
        format_map.setdefault("nginx_location_url", url_path)
        location_string = "\n"
        location_string.join(includes)
        location_string.join(set_headers)
        for key, value in configure.items():
            location_conf_line_string = f"{key} {value};".join("\n")
            location_string.join(location_conf_line_string)
        format_map.setdefault("nginx_location", location_string)
        module_data = ModuleData()
        nginx_location_conf_string = (
            module_data.nginx_location_conf_path.read_text().format_map(format_map)
        )

        return nginx_location_conf_string

    def nginx_server_configure(
        self,
        listen: str,
        server_name: str,
        root: str = "",
        index: str = "index index.html index.htm",
        certificates: str = "",
        access_log: str = "",
        error_log: str = "",
        locations: str = "",
    ) -> dict | None:
        configure = {}
        configure.setdefault("nginx_server_listen", listen)
        configure.setdefault("nginx_server_name", server_name)
        configure.setdefault("nginx_server_certificate", certificates)
        configure.setdefault("nginx_server_access_log", access_log)
        configure.setdefault("nginx_server_error_log", error_log)
        configure.setdefault("nginx_server_index", index)
        configure.setdefault("nginx_server_root", root)
        configure.setdefault("nginx_server_locations", locations)
        return configure

    def nginx_server_string(self, configure: dict) -> str | None:
        if not isinstance(configure, dict):
            return None

        module_data = ModuleData()
        nginx_server_string = module_data.nginx_server_conf_path.read_text().format_map(
            configure
        )
        return nginx_server_string

    def nginx_servers_string(
        self,
        servers: str,
        servers_head: str = "",
        servers_foot: str = "",
    ) -> str | None:
        if is_empty_string(servers):
            return None
        return f"{servers_head}\n{servers}\n{servers_foot}"

    def dumps(self, configure: list | dict) -> str | None:
        if not isinstance(configure, list) and not isinstance(configure, dict):
            return None
        configure_string = crossplane.build(configure)
        return configure_string

    def load(self, nginx_conf_path: Path) -> dict | None:
        if not isinstance(nginx_conf_path, Path) or not nginx_conf_path.exists():
            return None
        payload = crossplane.parse(nginx_conf_path)
