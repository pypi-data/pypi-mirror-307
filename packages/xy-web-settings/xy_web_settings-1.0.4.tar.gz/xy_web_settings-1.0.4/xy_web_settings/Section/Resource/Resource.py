# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Resource"
"""
  * @File    :   Resource.py
  * @Time    :   2023/11/09 15:55:35
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_web_settings.Section.Section import *


class Resource(Section):
    media_url: str | None = None

    media_path: Path | None = None

    static_url: str | None = None

    static_path: Path | None = None

    tmp_path: Path | None = None

    template_path: Path | None = None

    def _load(self):
        ########## sync_data ##########

        self.media_url = self._sync_data(
            "media_url",
            "/media/",
        )

        self.static_url = self._sync_data(
            "static_url",
            "/static/",
        )

        ########## fetch_path ##########

        self.media_path = self._fetch_path(
            "media_path",
            Path("../media/"),
        )

        self.static_path = self._fetch_path(
            "static_path",
            Path("../static/"),
        )

        self.tmp_path = self._fetch_path(
            "tmp_path",
            Path("../workspace/tmp/"),
        )

        self.template_path = self._fetch_path(
            "template_path",
            Path("../template/"),
        )

        super()._load()
