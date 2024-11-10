# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Mysql"
"""
  * @File    :   Mysql.py
  * @Time    :   2023/04/26 19:32:23
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""
from multiprocessing import Value
from mysql.connector import connect
from mysql.connector.connection_cext import CMySQLConnection
from xy_string.utils import is_empty_string
from xy_web_work.System.OS import OS, os_current


class Mysql:
    def stop_cmd_list(self, *args, **kwargs) -> list:
        cmd_list = []
        match os_current():
            case OS.Linux:
                cmd_list.append("sudo")
                cmd_list.append("service")
                cmd_list.append("mysql")
                cmd_list.append("stop")
            case OS.MacOS:
                cmd_list.append("mysql.server")
                cmd_list.append("stop")
        return cmd_list

    def start_cmd_list(self, *args, **kwargs) -> list:
        cmd_list = []
        match os_current():
            case OS.Linux:
                cmd_list.append("sudo")
                cmd_list.append("service")
                cmd_list.append("mysql")
                cmd_list.append("start")
            case OS.MacOS:
                cmd_list.append("mysql.server")
                cmd_list.append("start")
        return cmd_list

    def connect(
        self,
        password: str,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        db_name: str = "",
    ) -> CMySQLConnection | None:
        if (
            is_empty_string(password)
            or is_empty_string(host)
            or is_empty_string(user)
            or port < 0
        ):
            return None
        try:
            if is_empty_string(db_name):
                return connect(host=host, port=port, user=user, password=password)
            else:
                return connect(
                    host=host, port=port, user=user, password=password, database=db_name
                )
        except:
            return None
