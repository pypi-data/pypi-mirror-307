# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Search"
"""
  * @File    :   Search.py
  * @Time    :   2024/11/06 20:15:24
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

import re
from re import RegexFlag
from pathlib import Path
from xy_file.types import FileType


class Search:
    file_type: FileType = FileType.ANY
    work_dir: Path = Path.cwd()
    keyword: str = ""
    ignore_hidden_files: bool = True
    regex_flag: RegexFlag = re.M
    deep_start: int = 0
    # deep_start 0 => 绝对路径所有, -1 => 最后文件名.
    deep_count: int = -1
    # deep_count -1 => 递归所有, 0 => 仅当前, 1 => 当前+1级, 2 => 当前+2级, ...

    def validated_path(self, path: Path) -> Path | None:
        path_validate = self.file_type.validate(path=path)
        hidden_file_part = [part for part in path.parts if part.startswith(".")]
        is_hidden_file = not hidden_file_part or len(hidden_file_part) == 0
        ok = path_validate and not (
            is_hidden_file and self.ignore_hidden_files == False
        )
        if ok and path.exists():
            return path
        else:
            return None

    def deeped_path(self, path: Path) -> str:
        path_parts = None
        if self.deep_start == 0:
            path_parts = path.parts
        elif self.deep_start == -1:
            path_parts = path.parts[-1:]
        else:
            path_parts = path.parts[self.deep_start : self.deep_start + self.deep_count]
        if len(path_parts) > 0:
            path_str = "/".join(path_parts)
            if path_parts[0] == "/":
                path_str = path_str[1:]
            return path_str
        return ""

    def pattern(self) -> re.Pattern:
        return re.compile(
            self.keyword,
            flags=self.regex_flag,
        )

    def search(
        self,
        path: Path,
    ) -> bool:
        pattern = self.pattern()
        validated_path = self.validated_path(path)
        if isinstance(pattern, re.Pattern) and isinstance(validated_path, Path):
            deeped_path = self.deeped_path(validated_path)
            results = pattern.search(deeped_path)
            if results != None:
                return True
        return False
