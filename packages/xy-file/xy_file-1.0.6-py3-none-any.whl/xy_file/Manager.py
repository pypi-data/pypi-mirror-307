# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Manager"
"""
  * @File    :   Manager.py
  * @Time    :   2024/11/06 20:24:27
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""
import re
from re import RegexFlag
from pathlib import Path
import os
import shutil
from typing import Callable, Any
from xy_console.utils import *

from .Object.File import File
from .types import FileType
from .Operation.Rename import Rename
from .Operation.Search import Search


class Manager:

    def rglob_clean(
        self,
        keyword: str | None = None,
        work_dir: Path = Path.cwd(),
        file_type: FileType = FileType.ANY,
        ignore_hidden_files: bool = True,
        log_info=printt,
        log_error=print_e,
        log_success=print_s,
        should_delete_delegate: Callable[[list[Path]], bool] | None = None,
    ):
        if not log_info or not callable(log_info):
            log_info = printt
        if not log_error or not callable(log_error):
            log_error = printt
        if not log_success or not callable(log_success):
            log_success = printt

        if not os.access(work_dir, os.W_OK):  # type: ignore
            raise PermissionError(f"当前工作目录\n({work_dir})\n没有写入权限!!!")
        if not keyword:
            raise ValueError(
                "请传入关键字(-r)的参数进行过滤, -r支持Linux文件名通配符搜索",
            )
        file_path_list = []
        invalidate_file_path_list = []
        search_result = (
            list(work_dir.rglob(keyword))
            if isinstance(keyword, str)
            and isinstance(work_dir, Path)
            and work_dir.exists()
            else []
        )
        if (
            not search_result
            or not isinstance(search_result, list)
            or len(search_result) == 0
        ):
            log_info("暂无匹配文件或目录")
            return
        file_path_list = []
        invalidate_file_path_list = []
        for work_glob in search_result:
            search: Search = Search()
            search.keyword = keyword
            search.work_dir = work_dir
            search.file_type = file_type
            search.ignore_hidden_files = ignore_hidden_files
            validated_path = search.validated_path(work_glob)
            if isinstance(validated_path, Path):
                file_verbose_name = FileType.verbose_name(validated_path)
                msg = f"将要删除... => [{file_verbose_name}] {validated_path}"
                log_info(msg)
                file_path_list.append(validated_path)
            else:
                invalidate_file_path_list.append(validated_path)
        if not file_path_list:
            log_info("暂无匹配文件或目录")
            return
        validate_delegate = should_delete_delegate != None and callable(
            should_delete_delegate
        )
        should_delete = (
            validate_delegate and should_delete_delegate(file_path_list) == True
        )
        if should_delete == True:
            log_info("开始删除...")
            success_file_path_list = []
            fail_file_path_list = []
            for file_path in file_path_list:
                try:
                    file_verbose_name = FileType.verbose_name(file_path)
                    log_info(f"正在删除... => [{file_verbose_name}] {file_path} ")
                    if file_path.is_dir():
                        shutil.rmtree(file_path)
                    else:
                        file_path.unlink()
                    success_file_path_list.append(file_path)
                except:
                    fail_file_path_list.append(file_path)
            if not fail_file_path_list:
                log_success("全部删除完成 !!!")
            else:
                for file_path in fail_file_path_list:
                    file_verbose_name = FileType.verbose_name(file_path)
                    msg = f"还未删除... => [{file_verbose_name}] {file_path}"
                    log_error(msg)
                log_error(
                    f"还剩下以上文件或目录未删除(共计: {len(fail_file_path_list) if isinstance(fail_file_path_list, list) else 0}): ==>"
                )
                log_error("=" * 50)
        else:
            log_info("取消删除...")

    def search_clean(
        self,
        keyword: str | None = None,
        work_dir: Path = Path.cwd(),
        file_type: FileType = FileType.ANY,
        ignore_hidden_files: bool = True,
        deep_start: int = 0,  # 0 => 绝对路径所有, -1 => 最后文件名.
        deep_count: int = 0,  # -1 => 递归所有, 0 => 仅当前, 1 => 当前+1级, 2 => 当前+2级, ...
        regex_flag: RegexFlag = re.M,
        log_info=printt,
        log_error=print_e,
        log_success=print_s,
        should_delete_delegate: Callable[[list[Path]], bool] | None = None,
    ):
        if not log_info or not callable(log_info):
            log_info = printt
        if not log_error or not callable(log_error):
            log_error = printt
        if not log_success or not callable(log_success):
            log_success = printt

        if not os.access(work_dir, os.W_OK):  # type: ignore
            raise PermissionError(f"当前工作目录\n({work_dir})\n没有写入权限!!!")
        if not keyword:
            raise ValueError(
                "请传入关键字(-k)的参数进行过滤, -k支持正则表达式匹配符进行搜索",
            )
        file_path_list = []
        invalidate_file_path_list = []
        search_result = list(work_dir.rglob("**/*"))
        file_path_list = []
        invalidate_file_path_list = []
        for work_glob in search_result:
            search: Search = Search()
            search.keyword = keyword
            search.work_dir = work_dir
            search.file_type = file_type
            search.ignore_hidden_files = ignore_hidden_files
            search.deep_start = deep_start
            search.deep_count = deep_count
            search.regex_flag = regex_flag
            validated_path = search.validated_path(work_glob)
            if (
                isinstance(validated_path, Path)
                and search.search(validated_path) == True
            ):
                file_verbose_name = FileType.verbose_name(validated_path)
                msg = f"将要删除... => [{file_verbose_name}] {validated_path}"
                log_info(msg)
                file_path_list.append(validated_path)
            else:
                invalidate_file_path_list.append(validated_path)
        if not file_path_list:
            log_info("暂无匹配文件或目录")
            return
        validate_delegate = should_delete_delegate != None and callable(
            should_delete_delegate
        )
        should_delete = (
            validate_delegate and should_delete_delegate(file_path_list) == True
        )
        if should_delete == True:
            log_info("开始删除...")
            success_file_path_list = []
            fail_file_path_list = []
            for file_path in file_path_list:
                try:
                    file_verbose_name = FileType.verbose_name(file_path)
                    log_info(f"正在删除... => [{file_verbose_name}] {file_path} ")
                    if file_path.is_dir():
                        shutil.rmtree(file_path)
                    else:
                        file_path.unlink()
                    success_file_path_list.append(file_path)
                except:
                    fail_file_path_list.append(file_path)
            if not fail_file_path_list:
                log_success("全部删除完成 !!!")
            else:
                for file_path in fail_file_path_list:
                    file_verbose_name = FileType.verbose_name(file_path)
                    msg = f"还未删除... => [{file_verbose_name}] {file_path}"
                    log_error(msg)
                log_error(
                    f"还剩下以上文件或目录未删除(共计: {len(fail_file_path_list) if isinstance(fail_file_path_list, list) else 0}): ==>"
                )
                log_error("=" * 50)
        else:
            log_info("取消删除...")

    def rglob_files(
        self,
        keyword: str | None = None,
        work_dir: Path = Path.cwd(),
        file_type: FileType = FileType.ANY,
        ignore_hidden_files: bool = True,
        log_info=printt,
        log_error=print_e,
        log_success=print_s,
    ):
        if not log_info or not callable(log_info):
            log_info = printt
        if not log_error or not callable(log_error):
            log_error = printt
        if not log_success or not callable(log_success):
            log_success = printt

        if not os.access(work_dir, os.W_OK):  # type: ignore
            raise PermissionError(f"当前工作目录\n({work_dir})\n没有写入权限!!!")
        if not keyword:
            raise ValueError(
                "请传入关键字(-r)的参数进行过滤, -r支持Linux文件名通配符搜索",
            )
        file_path_list = []
        search_result = (
            list(work_dir.rglob(keyword))
            if isinstance(keyword, str)
            and isinstance(work_dir, Path)
            and work_dir.exists()
            else []
        )
        if (
            not search_result
            or not isinstance(search_result, list)
            or len(search_result) == 0
        ):
            log_info("暂无匹配对象")
            return
        file_path_list = []
        for work_glob in search_result:
            search: Search = Search()
            search.keyword = keyword
            search.work_dir = work_dir
            search.file_type = file_type
            search.ignore_hidden_files = ignore_hidden_files
            validated_path = search.validated_path(work_glob)
            if isinstance(validated_path, Path):
                file_verbose_name = FileType.verbose_name(validated_path)
                msg = f"查找到... => [{file_verbose_name}] {validated_path}"
                file_path_list.append(validated_path)
                log_info(msg)
        msg = f"匹配到 {len(file_path_list)} 个对象"
        if len(file_path_list) > 0:
            log_info(msg)
        else:
            log_info("暂无匹配对象")

    def search_files(
        self,
        keyword: str | None = None,
        work_dir: Path = Path.cwd(),
        file_type: FileType = FileType.ANY,
        ignore_hidden_files: bool = True,
        deep_start: int = 0,  # 0 => 绝对路径所有, -1 => 最后文件名.
        deep_count: int = -1,  # -1 => 递归所有, 0 => 仅当前, 1 => 当前+1级, 2 => 当前+2级, ...
        regex_flag: RegexFlag = re.M,
        log_info=printt,
        log_error=print_e,
        log_success=print_s,
    ):
        if not log_info or not callable(log_info):
            log_info = printt
        if not log_error or not callable(log_error):
            log_error = printt
        if not log_success or not callable(log_success):
            log_success = printt

        if not os.access(work_dir, os.W_OK):  # type: ignore
            raise PermissionError(f"当前工作目录\n({work_dir})\n没有写入权限!!!")
        if not keyword:
            raise ValueError(
                "请传入关键字(-k)的参数进行过滤, -k支持正则表达式匹配符进行搜索",
            )
        search_result = work_dir.rglob("**/*")
        file_path_list = []
        for result in search_result:
            search: Search = Search()
            search.keyword = keyword
            search.work_dir = work_dir
            search.file_type = file_type
            search.ignore_hidden_files = ignore_hidden_files
            search.deep_start = deep_start
            search.deep_count = deep_count
            search.regex_flag = regex_flag
            validated_path = search.validated_path(result)
            if (
                isinstance(validated_path, Path)
                and search.search(validated_path) == True
            ):
                file_verbose_name = FileType.verbose_name(validated_path)
                msg = f"查找到... => [{file_verbose_name}] {validated_path}"
                log_info(msg)
                file_path_list.append(validated_path)
        if not file_path_list:
            log_info("暂无匹配文件或目录")
            return

    def rename_files(
        self,
        work_dir: Path = Path.cwd(),
        source_pattern: str | None = None,
        replace: str | Callable[[Any], str] | None = None,
        deep_start: int = 0,  # 0 => 绝对路径所有, -1 => 最后文件名.
        deep_count: int = -1,  # -1 => 递归所有, 0 => 仅当前, 1 => 当前+1级, 2 => 当前+2级, ...
        count: int = 0,  # 匹配次数, 0 => 无限制, 其他按输入次数为匹配次数
        file_type: FileType = FileType.ANY,
        ignore_hidden_files: bool = True,
        regex_flag: RegexFlag = re.M,
        log_info=printt,
        log_error=print_e,
        log_success=print_s,
        should_rename_delegate: Callable[[dict[str, str]], bool] | None = None,
    ):
        if not log_info or not callable(log_info):
            log_info = printt
        if not log_error or not callable(log_error):
            log_error = printt
        if not log_success or not callable(log_success):
            log_success = printt

        if not os.access(work_dir, os.W_OK):  # type: ignore
            raise PermissionError(f"当前工作目录\n({work_dir})\n没有写入权限!!!")
        if not source_pattern:
            raise ValueError(
                "请传入 源文件表达式 (-s) 的参数进行过滤, -s支持正则表达式匹配符进行搜索",
            )
        if not replace:
            raise ValueError(
                "请传入 目标文件表达式 (-t) 的参数进行过滤, -s支持正则表达式匹配符进行搜索",
            )
        search_result = work_dir.rglob("**/*")
        result_map = {}
        for result in search_result:
            search: Search = Search()
            search.keyword = result.as_posix()
            search.work_dir = work_dir
            search.file_type = file_type
            search.ignore_hidden_files = ignore_hidden_files
            search.deep_start = deep_start
            search.deep_count = deep_count
            search.regex_flag = regex_flag
            validated_path = search.validated_path(result)
            if (
                isinstance(validated_path, Path)
                and search.search(validated_path) == True
            ):
                rename: Rename = Rename()
                rename.file_type = file_type
                rename.ignore_hidden_files = ignore_hidden_files
                rename.regex_flag = regex_flag
                validated_path = rename.validated_path(result)
                if isinstance(validated_path, Path):
                    file_verbose_name = FileType.verbose_name(validated_path)
                    new_result = rename.rename(
                        result,
                        source_pattern=source_pattern,
                        replace=replace,
                        deep_start=deep_start,
                        deep_count=deep_count,
                        count=count,
                    )
                    if isinstance(new_result, Path) and new_result != result:
                        msg = f"匹配到... => [{file_verbose_name}] {validated_path}\n修改为: ==> \n{new_result}"
                        log_info(msg)
                        result_map.update(
                            {
                                validated_path.as_posix(): new_result.as_posix(),
                            }
                        )
        if not result_map:
            log_info("暂无匹配对象")
            return
        validate_delegate = should_rename_delegate != None and callable(
            should_rename_delegate
        )
        should_rename = validate_delegate and should_rename_delegate(result_map) == True
        if should_rename == True:
            success_map = {}
            fail_map = {}
            for source, target in result_map.items():
                try:
                    cmd = f"mv {source} {target}"
                    result = os.system(cmd)
                    if result == 0:
                        success_map.update({source: target})
                    else:
                        fail_map.update({source: target})
                except:
                    fail_map.update({source: target})
        else:
            log_info("取消重命名")

    def random_touch(
        self,
        work_dir: Path = Path.cwd(),
        extension: str | None = "",
        locale: str = "en",
        log_info=printt,
        log_error=print_e,
        log_success=print_s,
        should_touch_delegate: Callable[[Path], bool] | None = None,
    ):
        if not log_info or not callable(log_info):
            log_info = printt
        if not log_error or not callable(log_error):
            log_error = printt
        if not log_success or not callable(log_success):
            log_success = printt

        if not os.access(work_dir, os.W_OK):  # type: ignore
            raise PermissionError(f"当前工作目录\n({work_dir})\n没有写入权限!!!")
        file_path = File.random_filename(
            work_dir=work_dir,
            extension=extension,
            locale=locale,
        )
        msg = f"生成新文件路径为:  ==> {file_path} "
        log_info(msg)
        validate_delegate = should_touch_delegate != None and callable(
            should_touch_delegate
        )
        should_touch = validate_delegate and should_touch_delegate(file_path) == True
        if should_touch == True:
            result = File.touch(file_path)
            if isinstance(result, Path) and result.exists():
                log_info(f"创建文件: \n{file_path} \n成功!!!")
            else:
                log_info(f"创建文件: \n{file_path} \n失败!!!")
        else:
            log_info("取消创建文件")

    def random_mkdir(
        self,
        work_dir: Path = Path.cwd(),
        extension: str | None = "",
        locale: str = "en",
        log_info=printt,
        log_error=print_e,
        log_success=print_s,
        should_mkdir_delegate: Callable[[Path], bool] | None = None,
    ):
        if not log_info or not callable(log_info):
            log_info = printt
        if not log_error or not callable(log_error):
            log_error = printt
        if not log_success or not callable(log_success):
            log_success = printt
        if not os.access(work_dir, os.W_OK):  # type: ignore
            raise PermissionError(f"当前工作目录\n({work_dir})\n没有写入权限!!!")

        file_path = File.random_filename(
            work_dir=work_dir,
            extension=extension,
            locale=locale,
        )
        msg = f"生成新目录路径为:  ==> {file_path} "
        log_info(msg)
        validate_delegate = should_mkdir_delegate != None and callable(
            should_mkdir_delegate
        )
        should_mkdir = validate_delegate and should_mkdir_delegate(file_path) == True
        if should_mkdir == True:
            result = File.mkdir(file_path)
            if isinstance(result, Path) and result.exists():
                log_info(f"创建目录: \n{file_path} \n成功!!!")
            else:
                log_info(f"创建目录: \n{file_path} \n失败!!!")
        else:
            log_info("取消创建目录")
