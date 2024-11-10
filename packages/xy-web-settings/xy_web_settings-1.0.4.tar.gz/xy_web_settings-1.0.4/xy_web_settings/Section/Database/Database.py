# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Database"
"""
  * @File    :   Database.py
  * @Time    :   2023/11/09 15:56:06
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_web_settings.Section.Section import *
from uuid import uuid4


class Database(Section):
    db_host: str | None = None

    db_port: int | None = None

    db_name: str | None = None

    db_user: str | None = None

    db_password: str | None = None

    db_path: Path | None = None

    db_file: Path | None = None

    backup_path: Path | None = None

    def _load(self):
        ########## sync_data ##########

        self.db_host = self._sync_data("db_host", "127.0.0.1")

        self.db_port = self._sync_data("db_port", 3306)

        self.db_name = self._sync_data("db_name", uuid4().hex[:10])

        self.db_user = self._sync_data("db_user", uuid4().hex[:10])

        self.db_password = self._sync_data("db_password", uuid4().hex[:10])

        ########## fetch_path ##########

        self.db_path = self._fetch_path(
            "db_path",
            Path("../workspace/database/"),
        )

        self.db_file = self._fetch_path(
            "db_file_path",
            Path("../workspace/database/xy_web.sqlite3"),
        )

        self.backup_path = self._fetch_path(
            "backup_path",
            Path("../workspace/backup/database/"),
        )

        super()._load()
