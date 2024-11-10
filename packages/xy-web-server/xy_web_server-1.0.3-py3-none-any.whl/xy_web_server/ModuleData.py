# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "ModuleData"
"""
  * @File    :   ModuleData.py
  * @Time    :   2023/04/26 15:02:59
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

import xy_web_server
from importlib_resources import files


class ModuleData:
    def __init__(self) -> None:
        self.path = files(xy_web_server.__name__).joinpath("data")

        self.template_path = self.path.joinpath("template")

        ############################## Config #############################

        self.config_path = self.template_path.joinpath("config")

        self.work_toml_template_path = self.config_path.joinpath(
            "xy_web_server_toml.template"
        )

        ############################## Runner #############################

        self.runner_path = self.template_path.joinpath("runner")

        self.runner_py_template_path = self.runner_path.joinpath("runner_py.template")
