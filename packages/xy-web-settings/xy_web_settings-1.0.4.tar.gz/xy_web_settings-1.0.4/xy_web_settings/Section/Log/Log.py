# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Log"
"""
  * @File    :   Log.py
  * @Time    :   2023/11/09 15:55:51
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_web_settings.Section.Section import *


class Log(Section):
    path: Path | None = None

    info_log: Path | None = None

    error_log: Path | None = None

    warn_log: Path | None = None

    def _load(self):
        ########## fetch_path ##########

        self.path = self._fetch_path(
            "path",
            Path("../workspace/logs/"),
        )

        self.info_log = self._fetch_path(
            "info_log",
            Path("../workspace/logs/info.log"),
        )

        self.error_log = self._fetch_path(
            "error_log",
            Path("../workspace/logs/error.log"),
        )

        self.warn_log = self._fetch_path(
            "warn_log",
            Path("../workspace/logs/warn.log"),
        )

        super()._load()
