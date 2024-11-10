# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Rename"
"""
  * @File    :   Rename.py
  * @Time    :   2024/11/06 20:15:37
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""
import re
from re import RegexFlag
from typing import Any, Callable, List
from pathlib import Path
from xy_file.types import FileType


class Rename:

    file_type: FileType = FileType.ANY
    ignore_hidden_files: bool = True
    regex_flag: RegexFlag = re.M

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

    def rename(
        self,
        file_path: Path | str | None = None,
        source_pattern: str | None = None,
        replace: str | Callable[[Any], str] | None = None,
        deep_start: int = 0,  # 0 => 绝对路径所有, -1 => 最后文件名.
        deep_count: int = -1,  # -1 => 递归所有, 0 => 仅当前, 1 => 当前+1级, 2 => 当前+2级, ...
        count: int = 0,  # 匹配次数, 0 => 无限次, 其余按照输入数量为匹配次数
    ) -> Path | None:
        if file_path == None or source_pattern == None or replace == None:
            return None
        if isinstance(file_path, str):
            file_path = Path(file_path)
        file_path = self.validated_path(file_path)
        if file_path == None:
            return None
        if isinstance(file_path, Path):
            file_path_parts = None
            if deep_start == 0:
                file_path_parts = file_path.parts
            elif deep_start == -1:
                file_path_parts = file_path.parts[-1:]
            else:
                file_path_parts = file_path.parts[deep_start : deep_start + deep_count]
            if len(file_path_parts) > 0:
                file_path = "/".join(file_path_parts)
                if file_path_parts[0] == "/":
                    file_path = file_path[1:]
        result = re.sub(
            source_pattern,
            replace,
            file_path,
            count=count,
            flags=self.regex_flag,
        )
        if result == None:
            return None
        return Path(result)
