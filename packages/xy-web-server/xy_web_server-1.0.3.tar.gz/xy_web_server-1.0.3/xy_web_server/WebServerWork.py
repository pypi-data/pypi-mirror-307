# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "WebServerWork"
"""
  * @File    :   WebServerWork.py
  * @Time    :   2023/04/25 23:03:56
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

import xy_web_server
from .Work import Work


class WebServerWork(Work):

    def __init__(self):
        self.quick_default_info(xy_web_server.__name__)
        self.description = "Web服务工作应用"
