# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Way"
"""
  * @File    :   Way.py
  * @Time    :   2023/04/26 03:02:04
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, Ship of Ocean
  * @Desc    :   None
"""

from enum import IntEnum


class Way(IntEnum):
    MYSQL = 0
    SQLITE = 1
    REDIS = 2
    POSTGRESQL = 3
    MONGO = 4
