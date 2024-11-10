# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "types"
"""
  * @File    :   types.py
  * @Time    :   2024/11/06 20:22:05
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""

from enum import IntEnum
from pathlib import Path


class FileType(IntEnum):
    ANY = 0
    FILE = 1
    DIR = 2
    SYMLINK = 3
    HARDLINK = 4
    SOCKET = 5
    CHAR_DEVICE = 6
    BLOCK_DEVICE = 7
    FIFO = 8

    @classmethod
    def parse(cls, file_type_filter: str | int | None):
        if not file_type_filter:
            return FileType.ANY

        names = [member for member in cls if member.name.upper() == file_type_filter]
        if names and len(names) > 0:
            return names[0]

        values = [member for member in cls if member.value == file_type_filter]
        if values and len(values) > 0:
            return values[0]

        return FileType.ANY

    def validate(self, path: Path) -> bool:
        if not path or not path.exists():
            return False
        match self:
            case FileType.ANY:
                return True
            case FileType.FILE:
                return path.is_file()
            case FileType.DIR:
                return path.is_dir()
            case FileType.SYMLINK:
                return path.is_symlink()
            case FileType.HARDLINK:
                return path.stat().st_nlink == 2
            case FileType.SOCKET:
                return path.is_socket()
            case FileType.CHAR_DEVICE:
                return path.is_char_device()
            case FileType.BLOCK_DEVICE:
                return path.is_block_device()
            case FileType.FIFO:
                return path.is_fifo()
            case _:
                return True

    @staticmethod
    def verbose_name(file_path: Path) -> str:
        file_type = "文件"
        if file_path.is_dir():
            file_type = "目录"
        elif file_path.is_symlink():
            file_type = "软链接"
        elif file_path.stat().st_nlink == 2:
            file_type = "硬连接"
        elif file_path.is_socket():
            file_type = "Socket"
        elif file_path.is_char_device():
            file_type = "字符设备(char_device)"
        elif file_path.is_block_device():
            file_type = "块设备(block_device)"
        elif file_path.is_fifo():
            file_type = "管道"
        else:
            file_type = "文件"
        return file_type
