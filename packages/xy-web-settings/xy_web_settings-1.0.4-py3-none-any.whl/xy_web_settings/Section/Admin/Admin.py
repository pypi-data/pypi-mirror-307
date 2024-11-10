# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Admin"
""" 
 * @Author: 余洋 yuyangit.0515@qq.com
 * @Date: 2024-10-21 12:20:21
 * @LastEditors: 余洋 yuyangit.0515@qq.com
 * @LastEditTime: 2024-10-21 12:32:51
 * @FilePath: /xy_web_settings/xy_web_settings/Section/Admin/Admin.py
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 """
"""
  * @File    :   Admin.py
  * @Time    :   2023/11/09 15:56:21
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_web_settings.Section.Section import *


class Admin(Section):
    name: str | None

    host: str | None

    debug_port: int | None

    release_port: int | None

    logs_path: Path | None

    admin_log: Path | None

    backup_path: Path | None

    def _load(self):
        ########## sync_data ##########

        self.name = self._sync_data("name", "Admin")

        self.host = self._sync_data("host", "0.0.0.0")

        self.debug_port = self._sync_data("debug_port", 8403)

        self.release_port = self._sync_data("release_port", 8404)

        ########## fetch_path ##########

        self.backup_path = self._fetch_path("backup_path", Path("../workspace/logs/admin/"))  # type: ignore

        self.logs_path = self._fetch_path("logs_path", Path("../workspace/logs/admin/admin.log"))  # type: ignore

        self.admin_log = self._fetch_path("admin_log", Path("../workspace/backup/admin/"))  # type: ignore

        super()._load()
