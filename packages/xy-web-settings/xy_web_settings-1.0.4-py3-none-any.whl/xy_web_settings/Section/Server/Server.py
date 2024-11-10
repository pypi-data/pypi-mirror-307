# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Server"
"""
  * @File    :   Server.py
  * @Time    :   2023/11/09 15:55:28
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_web_settings.Section.Section import *


class Server(Section):
    path: Path | None = None

    config_path: Path | None = None

    site_path: Path | None = None

    admin_path: Path | None = None

    logs_path: Path | None = None

    info_log: Path | None = None

    error_log: Path | None = None

    warn_log: Path | None = None

    def _load(self):
        ########## fetch_path ##########

        self.path = self._fetch_path(
            "path",
            Path("../workspace/server/"),
        )

        self.config_path = self._fetch_path(
            "config_path",
            Path("../workspace/server/config/"),
        )

        self.site_path = self._fetch_path(
            "site_path",
            Path("../workspace/server/site/"),
        )

        self.admin_path = self._fetch_path(
            "admin_path",
            Path("../workspace/server/admin/"),
        )

        self.logs_path = self._fetch_path(
            "logs_path",
            Path("../workspace/logs/server/"),
        )

        self.info_log = self._fetch_path(
            "info_log",
            Path("../workspace/logs/server/info.log"),
        )

        self.error_log = self._fetch_path(
            "error_log",
            Path("../workspace/logs/server/error.log"),
        )

        self.warn_log = self._fetch_path(
            "warn_log",
            Path("../workspace/logs/server/warn.log"),
        )

        super()._load()
