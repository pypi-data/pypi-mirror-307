# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "OS"
"""
  * @File    :   OS.py
  * @Time    :   2023/04/26 20:45:54
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""

from enum import StrEnum
import platform


class OS(StrEnum):
    Uknown = "Unknown"
    Linux = "Linux"
    MacOS = "Darwin"
    Windows = "Windows"
    Android = "Android"


def os_current() -> OS:
    try:
        return OS(platform.system())
    except:
        return OS.Uknown
