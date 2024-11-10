# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Site"
"""
  * @File    :   Site.py
  * @Time    :   2023/11/09 15:55:12
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_web_settings.Section.Section import *
from uuid import uuid4


class Site(Section):
    host: str | None = None

    debug_port: int | None = None

    release_ports: list | None = [
        8401,
        8402,
    ]

    cookie_secret: str | None = None

    login_url: str | None = None

    logs_path: Path | None = None

    info_log: Path | None = None

    error_log: Path | None = None

    warn_log: Path | None = None

    backup_path: Path | None = None

    def _load(self):
        ########## sync_data ##########

        self.host = self._sync_data("host", "0.0.0.0")

        self.debug_port = self._sync_data("debug_port", 8400)

        self.cookie_secret = self._sync_data("cookie_secret", uuid4().hex)

        self.login_url = self._sync_data("login_url", "/site/user/login")

        ########## fetch_path ##########

        self.backup_path = self._fetch_path(
            "backup_path",
            Path("../workspace/backup/site/"),
        )

        self.logs_path = self._fetch_path(
            "logs_path",
            Path("../workspace/logs/site/"),
        )

        self.info_log = self._fetch_path(
            "info_log",
            Path("../workspace/logs/site/info.log"),
        )

        self.error_log = self._fetch_path(
            "error_log",
            Path("../workspace/logs/site/error.log"),
        )

        self.warn_log = self._fetch_path(
            "warn_log",
            Path("../workspace/logs/site/warn.log"),
        )

        super()._load()
