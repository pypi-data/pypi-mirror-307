# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Nginx"
"""
  * @File    :   Nginx.py
  * @Time    :   2023/11/09 15:55:43
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_web_settings.Section.Section import *


class Nginx(Section):
    path: Path | None = None

    logs_path: Path | None = None

    error_log: Path | None = None

    access_log: Path | None = None

    def _load(self):
        ########## fetch_path ##########

        self.path = self._fetch_path(
            "path",
            Path("../workspace/nginx/"),
        )

        self.logs_path = self._fetch_path(
            "logs_path",
            Path("../workspace/nginx/logs/"),
        )

        self.error_log = self._fetch_path(
            "error_log",
            Path("../workspace/nginx/logs/error.log"),
        )

        self.access_log = self._fetch_path(
            "access_log",
            Path("../workspace/nginx/logs/access.log"),
        )

        super()._load()
