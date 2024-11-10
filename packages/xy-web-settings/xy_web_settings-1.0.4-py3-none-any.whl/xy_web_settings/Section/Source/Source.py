# -*- coing: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Source"
"""
  * @File    :   Source.py
  * @Time    :   2023/11/09 15:54:57
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from pathlib import Path
from xy_file.Object.File import File
from xy_web_settings.Section.Section import *


class Source(Section):
    path: Path | None = None

    library_path: Path | None = None

    test_path: Path | None = None

    server_path: Path | None = None

    def _load(self):
        ########## fetch_path ##########
        self.path = self._fetch_path("path", Path("../source/"))
        self.library_path = self._fetch_path("library_path", Path("../source/Library/"))
        if self.auto_create_path and self.library_path:
            File.touch(self.library_path.joinpath("__init__.py"))
        self.test_path = self._fetch_path("test_path", Path("../workspace/test/"))
        if self.auto_create_path and self.test_path:
            File.touch(self.test_path.joinpath("__init__.py"))
        self.server_path = self._fetch_path("server_path", Path("../source/Server"))
        if self.auto_create_path and self.server_path:
            File.touch(self.server_path.joinpath("__init__.py"))
        super()._load()
