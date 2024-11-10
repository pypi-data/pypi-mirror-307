# -*- coding: UTF-8 -*-
__author__ = "余洋"
"""
  * @File    :   File.py
  * @Time    :   2023/04/22 19:25:26
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   None
"""

import logging
from pathlib import Path
from faker import Faker


class File:
    @staticmethod
    def random_filename(
        work_dir: Path,
        extension: str | None = None,
        locale="en",
    ) -> Path:
        faker = Faker(locale=locale)
        file_name = faker.file_name(extension=extension)
        file_path = work_dir.joinpath(file_name)
        if file_path.exists() == True:
            return File.random_filename(
                work_dir,
                extension=extension,
                locale=locale,
            )
        return file_path

    @staticmethod
    def random_touch(
        work_dir: Path,
        extension: str | None = None,
        locale="en",
    ) -> Path | None:
        file_path = File.random_filename(
            work_dir=work_dir,
            extension=extension,
            locale=locale,
        )
        return File.touch(file_path)

    @staticmethod
    def random_mkdir(
        work_dir: Path,
        extension: str | None = "",
        locale="en",
    ) -> Path | None:
        dir_path = File.random_filename(
            work_dir=work_dir,
            extension=extension,
            locale=locale,
        )
        return File.mkdir(dir_path)

    @staticmethod
    def touch(
        file_path: Path | str | None,
        force: bool = True,
    ) -> Path | None:
        if not file_path:
            return None

        if isinstance(file_path, str):
            file_path = Path(file_path)

        if isinstance(file_path, Path) and file_path.exists():
            return file_path

        try:
            if force:
                file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()
            return file_path.resolve()
        except Exception as exception:
            logging.exception(exception)
            return None

    @staticmethod
    def mkdir(
        file_path: Path | str | None,
        parents: bool = True,
        exist_ok: bool = True,
    ) -> Path | None:
        if not file_path:
            return None

        if isinstance(file_path, str):
            file_path = Path(file_path)

        if isinstance(file_path, Path) and file_path.exists():
            return file_path
        try:
            file_path.mkdir(
                parents=parents,
                exist_ok=exist_ok,
            )
            return file_path.resolve()
        except Exception as exception:
            logging.exception(exception)
            return None
