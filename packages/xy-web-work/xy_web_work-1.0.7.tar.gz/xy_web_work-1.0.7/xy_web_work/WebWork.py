# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "WebWork"
"""
  * @File    :   WebWork.py
  * @Time    :   2023/04/26 12:35:27
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""
from pathlib import Path
import xy_web_work
from .Work import Work


class WebWork(Work):
    config_relative_path: Path = Path("config/xy_web_work.toml")

    def __init__(self):
        self.quick_default_info(xy_web_work.__name__)
        self.description = "Web工作应用"
