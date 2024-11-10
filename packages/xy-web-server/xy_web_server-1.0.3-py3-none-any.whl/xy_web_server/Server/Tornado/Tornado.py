# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Tornado"
"""
  * @File    :   Tornado.py
  * @Time    :   2023/04/26 01:06:15
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""
import asyncio
import getpass
import os
from pathlib import Path
from xy_file.Object.File import File
from xy_type.utils import empty_value
from xy_string.utils import is_empty_string, contains_zh

from xy_web_server.ModuleData import ModuleData
from tornado.web import Application
from tornado.httpserver import HTTPServer


class Tornado:
    def default_supervisor_configure(
        self,
        command_string: str,
        directory: Path,
        env: str = "",
        extension: dict = {},
    ) -> dict | None:
        if is_empty_string(command_string):
            return None
        if not isinstance(directory, Path) or not directory.exists():
            return None
        configure = {}
        configure.setdefault("command", command_string)
        configure.setdefault("directory", str(directory))
        configure.setdefault("user", str(getpass.getuser()))
        configure.setdefault("autorestart", "true")
        configure.setdefault("redirect_stderr", "true")
        configure.setdefault("stdout_logfile", "")
        configure.setdefault("stderr_logfile", "")
        configure.setdefault("loglevel", "info")
        configure.setdefault("environment", env)
        configure.update(extension)
        return configure

    def default_application_settings(self) -> dict:
        settings = {
            "template_path": "",
            "debug": True,
            "cookie_secret": "",
            "xsrf_cookies": True,
            "autoreload": True,
            "login_url": "",
            "static_path": "",
        }

        return settings

    def make_server(
        self,
        application: Application,
        bind: int = 8080,
        cpu_count: int = 0,
    ) -> HTTPServer | None:
        if not application or bind < 0:
            return None
        server = HTTPServer(application)
        server.bind(bind)
        server.start(cpu_count)
        return server

    async def sync_make_application(self, urls: list, settings: dict, bind: int = 8080):
        application = self.make_application(urls, settings)
        if not application or bind <= 0:
            raise Exception(
                f"启动Tornado程序失败!!!, \n urls: urls = {urls} ,\n settings = {settings} ,\n 绑定端口: bind = {bind} \n"
            )
        else:
            application.listen(bind)
            await asyncio.Event().wait()

    def make_application(self, urls: list, settings: dict) -> Application:
        urls = empty_value(urls, list, [])
        settings = empty_value(settings, dict, {})
        return Application(urls, **settings)

    def create_site_app(self, dest_path: Path, name: str, *args, **kwargs) -> bool:
        if is_empty_string(name) or contains_zh(name):
            raise TypeError("请传入合法名称, 名称仅支持英文")
        if not isinstance(dest_path, Path):
            raise TypeError("请传入合法目的路径")
        if not dest_path.exists():
            raise FileNotFoundError("目的路径不存在,请传入存在的目的路径")
        if not os.access(dest_path, os.W_OK):
            raise PermissionError(f"目的路径没有写入权限: => ({dest_path})")
        module_data = ModuleData()
        site_application_tornado_path = module_data.site_application_tornado_path
        request_handlers_py_template_path = site_application_tornado_path.joinpath(
            "request_handlers_py.template"
        )
        urls_py_template_path = site_application_tornado_path.joinpath(
            "urls_py.template"
        )
        site_app_path = dest_path.joinpath(name)
        site_app_path.mkdir(parents=True, exist_ok=True)
        try:
            request_handlers_py_path = File.touch(
                site_app_path.joinpath("RequestHandlers.py")
            )
            urls_py_path = File.touch(site_app_path.joinpath("urls.py"))
            request_handerls_py_string = (
                request_handlers_py_template_path.read_text().format(site_app_name=name)
            )
            urls_py_string = urls_py_template_path.read_text().format(
                site_app_url=f"{name}"
            )
            request_handlers_py_path.write_text(request_handerls_py_string)
            urls_py_path.write_text(urls_py_string)
            return True
        except:
            site_app_path.rmdir()
            raise IOError("创建应用文件失败")

        return False
