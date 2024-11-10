# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "ModuleData"
"""
  * @File    :   ModuleData.py
  * @Time    :   2023/04/25 22:27:28
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""

from pathlib import Path

from importlib_resources import files

import xy_web_work


class ModuleData:
    def __init__(self) -> None:
        self.path = files(xy_web_work.__name__).joinpath("data")
        self.template_path = self.path.joinpath("template")

        ############################## Config #############################

        self.config_path = self.template_path.joinpath("config")

        self.work_toml_template_path = self.config_path.joinpath(
            "xy_web_work_toml.template"
        )

        ############################## Runner #############################

        self.runner_path = self.template_path.joinpath("runner")

        self.runner_py_template_path = self.runner_path.joinpath("runner_py.template")
