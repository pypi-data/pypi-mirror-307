# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Backup"
"""
  * @File    :   Backup.py
  * @Time    :   2023/11/09 15:56:14
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_web_settings.Section.Section import *


class Backup(Section):
    path: Path | None = None

    def _load(self):
        ########## fetch_path ##########

        self.path = self._fetch_path("path", Path("../workspace/backup/"))

        super()._load()
