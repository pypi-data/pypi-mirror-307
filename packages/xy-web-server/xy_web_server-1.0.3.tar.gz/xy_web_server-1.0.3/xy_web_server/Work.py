# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Work"
"""
  * @File    :   Work.py
  * @Time    :   2023/04/26 12:43:35
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

from xy_web_work.WebWork import WebWork as xyWebWork
from .Settings.Settings import Settings
from .ModuleData import ModuleData


class Work(xyWebWork):
    settings: Settings | None = Settings()
    module_data: ModuleData = ModuleData()
