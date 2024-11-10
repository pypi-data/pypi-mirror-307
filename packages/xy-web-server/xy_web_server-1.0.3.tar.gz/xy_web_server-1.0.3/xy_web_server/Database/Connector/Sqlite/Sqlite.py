# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Sqlite"
"""
  * @File    :   Sqlite.py
  * @Time    :   2023/04/26 19:32:32
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""
import os
from sqlite3 import connect
from sqlite3 import Connection
from pathlib import Path


class Sqlite:
    def connect(
        self,
        db_file_path: Path,
    ) -> Connection | None:
        if not isinstance(db_file_path, Path) or not os.access(
            db_file_path.parent, os.W_OK
        ):
            return None
        try:
            return connect(db_file_path)
        except:
            return None
