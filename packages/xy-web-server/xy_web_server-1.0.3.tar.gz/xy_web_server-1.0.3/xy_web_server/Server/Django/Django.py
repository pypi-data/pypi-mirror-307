# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Django"
"""
  * @File    :   Django.py
  * @Time    :   2023/04/26 01:05:52
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""
import os
from pathlib import Path
import django

from xy_string.utils import is_empty_string


class Django:
    def load(self, django_project_settings: str, allow_async: bool = True):
        if not isinstance(django_project_settings, str):
            return
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_project_settings)
        if allow_async is True:
            os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
        django.setup()

    def start_cmd_list(
        self,
        manage_path: Path,
        host: str = "0.0.0.0",
        port: int = 8080,
        python_path: str = "python",
    ) -> list | None:
        if (
            (isinstance(manage_path, Path) and not manage_path.exists())
            or not os.access(manage_path, os.X_OK)
            or is_empty_string(python_path)
            or is_empty_string(host)
            or port < 0
        ):
            return None
        manage_cmd: str = "runserver"
        cmd_list = []
        cmd_list.append(python_path)
        cmd_list.append(str(manage_path))
        cmd_list.append(manage_cmd)
        cmd_list.append(f"{host}:{port}")
        return cmd_list

    def default_quick_uwsgi_section(
        self,
        chdir: str = "",
        protocol: str = "",
        host_and_port: str = "",
        master: str = "true",
        pidfile: str = "",
        process: str = "1",
        worker: str = "1",
        plugin: str = "",
        pp: str = "",
        env: str = "",
        wsgi_file: str = "",
        module: str = "",
        profiler: str = "true",
        pcre_jit: str = "true",
        memory_report: str = "true",
        enable_threds: str = "true",
        limit_as: str = "2048",
        thunder_lock: str = "true",
        chmod_socket: str = "666",
        vacuum: str = "true",
        daemonize: str = "",
    ) -> dict | None:
        if is_empty_string(host_and_port):
            return None
        section = {}
        section.setdefault("chdir", chdir)
        if not protocol:
            protocol = "socket"
        section.setdefault(protocol, host_and_port)
        section.setdefault("master", master)
        section.setdefault("pidfile", pidfile)
        section.setdefault("process", process)
        section.setdefault("worker", worker)
        section.setdefault("plugin", plugin)
        section.setdefault("pp", pp)
        section.setdefault("env", env)
        section.setdefault("wsgi-file", wsgi_file)
        section.setdefault("module", module)
        section.setdefault("profiler", profiler)
        section.setdefault("pcre-jit", pcre_jit)
        section.setdefault("memory-report", memory_report)
        section.setdefault("enable-threads", enable_threds)
        section.setdefault("limit-as", limit_as)
        section.setdefault("thunder-lock", thunder_lock)
        section.setdefault("chmod-socket", chmod_socket)
        section.setdefault("vacuum", vacuum)
        section.setdefault("daemonize", daemonize)

        return section

    def default_uwsgi_section(
        self,
        protocol: "",
        host_and_port="",
    ) -> dict | None:
        if is_empty_string(host_and_port):
            return None
        if is_empty_string(protocol):
            protocol = "socket"
        section = {
            "chdir": "",
            protocol: host_and_port,
            "master": "true",
            "pidfile": "",
            "process": "1",
            "worker": "1",
            "plugin": "",
            "pp": "",
            "env": "",
            "wsgi-file": "",
            "module": "",
            "profiler": "true",
            "pcre-jit": "true",
            "memory-report": "true",
            "enable-threds": "true",
            "limit-as": "2048",
            "thunder-lock": "true",
            "chmod-socket": "666",
            "vacuum": "true",
            "daemonize": "",
        }

        return section

    def manage_cmd_list(
        self,
        manage_path: Path,
        python: str = "python",
        manage_cmd_list: list = [],
        *args,
        **kwargs,
    ) -> list | None:
        if (
            is_empty_string(str(manage_path))
            or (isinstance(manage_path, Path) and not manage_path.exists())
            or not os.access(manage_path, os.X_OK)
        ):
            return None
        if not isinstance(python, str):
            python = "python"
        cmd_list = []
        cmd_list.append(python)
        cmd_list.append(str(manage_path))
        cmd_list.extend(manage_cmd_list)
        return cmd_list

    def admin_cmd_list(
        self,
        django_admin_path: str = "django-admin",
        django_cmd: str = "help",
        *args,
        **kwargs,
    ) -> list:
        if is_empty_string(django_admin_path):
            django_admin_path = "django-admin"
        if is_empty_string(django_cmd):
            django_cmd = "help"
        cmd_list = [str(django_admin_path), django_cmd]
        return cmd_list
