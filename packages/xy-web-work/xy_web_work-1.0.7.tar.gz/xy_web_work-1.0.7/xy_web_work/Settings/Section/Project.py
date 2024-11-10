# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Project"
"""
  * @File    :   Project.py
  * @Time    :   2023/04/25 22:50:59
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""

from xy_work.Settings.Section.Project import Project as xyProject
from .Section import Section


class Project(Section, xyProject):
    def get_name(self) -> str | None:
        return "project"
