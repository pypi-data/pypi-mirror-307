# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Settings"
"""
  * @File    :   Settings.py
  * @Time    :   2023/04/25 22:30:24
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""

from pathlib import Path
from xy_web_settings.Settings import Settings as xySettings
from .Section.Project import Project
from .Section.Runner import Runner


class Settings(xySettings):
    default_cfg_relative_path: Path = Path("config/xy_web_work.toml")
    project: Project | None = Project()
    runner: Runner | None = Runner()

    def reload(self, settings_cfg_path: Path):
        super().reload(settings_cfg_path)
        self.project = self.make_section(Project)
        self.runner = self.make_section(Runner)
