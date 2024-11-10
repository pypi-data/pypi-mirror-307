# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Work"
"""
  * @File    :   Work.py
  * @Time    :   2023/04/24 14:11:41
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""

from xy_work.Work import Work as xyWork
from .ModuleData import ModuleData
from .Settings.Settings import Settings


class Work(xyWork):
    settings: Settings | None = Settings()
    module_data: ModuleData = ModuleData()
