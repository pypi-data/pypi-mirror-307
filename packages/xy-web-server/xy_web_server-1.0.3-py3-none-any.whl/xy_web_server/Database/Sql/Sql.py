# -*- coding: UTF-8 -*-
__author__ = '余洋'
__doc__ = 'Sql'
'''
  * @File    :   Sql.py
  * @Time    :   2023/04/26 20:27:13
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
'''

from xy_string.utils import is_empty_string

class Sql:
    
    def sql_user_database(self, db_name: str) -> str | None:
        if is_empty_string(db_name):
            return None
        return f"use {db_name}"

    def sql_flush_privileges(self) -> str:
        return "flush privileges"

    def sql_create_user(
        self,
        user: str,
        password: str,
        host: str = "%",
    ) -> str | None:
        if is_empty_string(user) or is_empty_string(password) or is_empty_string(host):
            return None
        sql = f"create user '{user}'@'{host}' identified by '{password};"
        return sql

    def sql_create_table(self, table_name: str, table_map: str) -> str | None:
        if is_empty_string(table_name) or is_empty_string(table_map):
            return None
        return f"create table {table_name} {table_map};"

    def sql_update(
        self, table_name: str, set_key: str, set_value: str, where_condition: str
    ) -> str | None:
        if (
            is_empty_string(table_name)
            or is_empty_string(set_key)
            or is_empty_string(set_value)
            or is_empty_string(where_condition)
        ):
            return None
        return (
            f"update {table_name} set {set_key} = {set_value} where {where_condition};"
        )

    def sql_create_database(
        self,
        db_name: str,
        if_not_exists: bool = True,
        encoding: str = "utf8",
    ) -> str | None:
        if is_empty_string(db_name):
            return None
        if_not_exists_string = ""
        if if_not_exists:
            if_not_exists_string = "if not exists"
        encoding_string = ""
        if not is_empty_string(encoding):
            encoding_string = f"default character set {encoding}"
        return f"create database {if_not_exists_string} {db_name} {encoding_string};"

    def sql_grant_privileges_on_to(self, privileges: str = "all privileges", on: str, to: str) -> str | None:
        if is_empty_string(privileges) or is_empty_string(on) or is_empty_string(to):
            return None
        return f"grant {privileges} on {on} to {to};"