# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "Runner"
"""
  * @File    :   Runner.py
  * @Time    :   2024/11/05 21:42:24
  * @Author  :   余洋
  * @Version :   0.0.1
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   
"""
import re
from argparse import Namespace
from pathlib import Path

import xy_file
from xy_argparse.ArgParse import ArgParse
from xy_console.utils import print_e, print_s, inputt, print_r, print_w

from .types import FileType
from .Manager import Manager
from .Object.File import File


class Runner(ArgParse):
    manager = Manager()

    def __init__(
        self,
        *args,
    ):
        self.quick_default_info(xy_file.__name__)
        self.description = "文件管理应用"

    def main(self):
        self.default_parser()
        self.add_arguments()
        self.run_arguments()

    def add_arguments(self):
        self.add_argument(
            "-w",
            "--work",
            help_text="""
                命令:
                clean | c => 常用清理文件或目录,通配符匹配, 配合 -r/--rglob-keyword 使用, 默认 **/*, 表示当前目录下所有匹配的文件和目录;
                search_clean | sc => 正则表达式搜索文件或目录来清理文件或目录, 配合 -k/--keyword 使用, 必须符合正则表达式;
                rglob_files | rf => 通配符匹配文件或目录, 配合 -r/--rglob-keyword 使用, 默认 **/*, 表示当前目录下所有匹配的文件和目录;
                search_files | sf => 正则表达式搜索文件或目录,, 配合 -k/--keyword 使用, 必须符合正则表达式;
                rename_files | r => 正则表达式匹配来重命名文件或目录, 配合 -k/--keyword 使用, 必须符合正则表达式;
                random_touch | rt => 创建随机文件;
                random_mkdir | rm => 创建随机目录, 默认会生成带后缀的文件名, 使用 (xy_file -w rm -e "") 来创建不带后缀的随机目录;
                random_file_name | rfn => 生成随机文件路径;
            """,
            required=True,
        )
        self.add_argument(
            "-y",
            "--yes",
            type_name=bool,
            help_text="随便填写-y开头的参数如: -yy.就会强制运行, 所有过程遇到提示都默认为Yes;",
            default=False,
        )
        self.add_argument(
            "-d",
            "--work-dir",
            help_text="工作目录, 默认当前工作目录, Path.cwd();",
        )
        self.add_argument(
            "-r",
            "--rglob-keyword",
            help_text="""
            通配符
            工作目录过滤匹配关键字; 
            默认: **/*, 当前目录下的全部文件和目录，
            可选，工作目录过滤关键字，使用通配符进行匹配，例如 *.py表示当前目录下所有py脚本""",
            default="**/*",
        )
        self.add_argument(
            "-k",
            "--keyword",
            help_text="关键字; 可选; 使用正则表达式Search, Rename; 默认: re.M模式, !!! 注意: 该关键字匹配是绝对路径字符串",
        )
        self.add_argument(
            "-regf",
            "--regex-flag",
            type_name=int,
            help_text="匹配模式: 2 => re.I, 8 => re.M, 16 => re.S, 32 => re.U, 64 => re.X",
            default=re.M.value,
        )
        self.add_argument(
            "-i",
            "--ignore-hidden-files",
            type_name=bool,
            help_text="""是否忽略隐藏目录和文件""",
            default=1,
        )
        self.add_argument(
            "-f",
            "--file-type-filter",
            type_name=int,
            help_text="""
                            过滤器, 默认为0; 无限制,
                            !!! 若输入字符串则无大小写限制,
                            以下为过滤器对应类型:
                            任意 = [0, any],
                            文件 = [1, file],
                    目录/文件夹 = [2, dir],
                        软链接 = [3, symlink],
                        硬链接 = [4, hardlink],
                        Socket = [5, socket],
            字符设备(char device) = [6, char_device],
            块设备(block device) = [7, block_device],
                    管道(fifo) = [8, fifo],
                            """,
            default=0,
        )
        self.add_argument(
            "-e",
            "--extension",
            help_text="文件后缀, 用于随机生成文件或目录",
        )
        self.add_argument(
            "-l",
            "--locale",
            help_text="语言环境, 默认英文 => en, 简体中文 => zh_CN",
        )
        self.add_argument(
            "-ds",
            "--deep-start",
            type_name=int,
            help_text="路径深度:  0 => 绝对路径所有, -1 => 最后文件名.",
            default=0,
        )
        self.add_argument(
            "-dc",
            "--deep-count",
            type_name=int,
            help_text="递归深度:  -1 => 递归所有, 0 => 仅当前, 1 => 当前+1级, 2 => 当前+2级, ...",
            default=-1,
        )
        self.add_argument(
            "-t",
            "--count",
            type_name=int,
            help_text="匹配次数, 0 => 无限制, 其他按输入次数为匹配次数",
            default=0,
        )
        self.add_argument(
            "-sp",
            "--source-pattern",
            help_text="源匹配式, 需符合正则表达式",
        )
        self.add_argument(
            "-rp",
            "--replace",
            help_text="目标匹配式, 需符合正则表达式",
        )

    @property
    def yes(self) -> bool:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            yes = arguments.yes
            if yes == None:
                return False
            return yes
        return False

    @property
    def work(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.work
        return None

    @property
    def work_dir(self) -> str | None:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.work_dir
        return None

    @property
    def rglob_keyword(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.rglob_keyword
        return None

    @property
    def keyword(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.keyword
        return None

    @property
    def regex_flag(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.regex_flag
        return re.M.value

    @property
    def ignore_hidden_files(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.ignore_hidden_files
        return True

    @property
    def file_type_filter(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.file_type_filter
        return FileType.ANY.value

    @property
    def extension(self) -> str | None:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.extension
        return None

    @property
    def locale(self) -> str | None:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.locale
        return "en"

    @property
    def deep_start(self) -> int | None:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.deep_start
        return 0

    @property
    def deep_count(self) -> int | None:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.deep_count
        return -1

    @property
    def count(self) -> int | None:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.count
        return 0

    @property
    def source_pattern(self) -> str | None:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.source_pattern
        return None

    @property
    def replace(self) -> str | None:
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.replace
        return None

    def on_arguments(self, name, value, arguments=None):
        rglob_keyword = self.rglob_keyword
        keyword = self.keyword
        file_type_filter = self.file_type_filter
        file_type = FileType.parse(file_type_filter)
        ignore_hidden_files = bool(self.ignore_hidden_files)
        deep_start = self.deep_start if isinstance(self.deep_start, int) else 0
        deep_count = self.deep_count if isinstance(self.deep_count, int) else -1
        count = self.count if isinstance(self.count, int) else 0
        extension = self.extension
        yes = self.yes if isinstance(self.yes, bool) else False
        regex_flag = (
            re.RegexFlag(self.regex_flag) if isinstance(self.regex_flag, int) else re.M
        )
        source_pattern = (
            self.source_pattern
            if isinstance(self.source_pattern, str) and self.source_pattern
            else self.source_pattern
        )
        replace = (
            self.replace
            if isinstance(self.replace, str) and self.replace
            else self.replace
        )
        locale = self.locale if isinstance(self.locale, str) else "en"
        work_dir = self.work_dir
        if work_dir == None:
            work_dir = Path.cwd()
        if not isinstance(work_dir, Path):
            work_dir = Path(work_dir)
        if name == "work":
            if value == "random_file_name" or value == "rfn":
                if Path(work_dir).exists() == False:
                    print_e(
                        "工作目录不存在, 随机生成文件名失败, 请传入-d/--work-dir参数为工作目录"
                    )
                    return
                randome_file_name = File.random_filename(
                    work_dir=work_dir,
                    extension=extension,
                )
                print_s(f"生成新的随机文件路径 => {randome_file_name}")
                print()
            elif value == "random_touch" or value == "rt":
                if Path(work_dir).exists() == False:
                    print_e(
                        "工作目录不存在, 随机生成文件失败, 请传入-d/--work-dir参数为工作目录"
                    )
                    return

                def should_touch_delegate(path: Path) -> bool:
                    if yes == True:
                        return True
                    print_w("是否创建以上文件?")
                    should_touch = inputt(
                        "确定请输入Y, 输入其他为取消创建命令. 请输入[Y/n]\n"
                    )
                    if should_touch == "Y":
                        return True
                    return False

                self.manager.random_touch(
                    Path.cwd(),
                    extension=extension,
                    locale=locale if locale else "en",
                    should_touch_delegate=should_touch_delegate,
                )
            elif value == "random_mkdir" or value == "rm":
                if Path(work_dir).exists() == False:
                    print_e(
                        "工作目录不存在, 随机生成目录失败, 请传入-d/--work-dir参数为工作目录"
                    )
                    return

                def should_mkdir_delegate(path: Path) -> bool:
                    if yes == True:
                        return True
                    print_w("是否创建以上目录?")
                    should_mkdir = inputt(
                        "确定请输入Y, 输入其他为取消创建命令. 请输入[Y/n]\n"
                    )
                    if should_mkdir == "Y":
                        return True
                    return False

                self.manager.random_mkdir(
                    work_dir,
                    extension=extension,
                    locale=locale if locale else "en",
                    should_mkdir_delegate=should_mkdir_delegate,
                )
            elif value == "rglob_files" or value == "rf":
                if Path(work_dir).exists() == False:
                    print_e(
                        "工作目录不存在, 通配符匹配搜索文件失败, 请传入-d/--work-dir参数为工作目录"
                    )
                    return
                self.manager.rglob_files(
                    keyword=rglob_keyword,
                    work_dir=work_dir,
                    file_type=file_type,
                    ignore_hidden_files=ignore_hidden_files,
                )
            elif value == "search_files" or value == "sf":
                if Path(work_dir).exists() == False:
                    print_e(
                        "工作目录不存在, 正则表达式搜索文件失败, 请传入-d/--work-dir参数为工作目录"
                    )
                    return
                self.manager.search_files(
                    keyword=keyword,
                    work_dir=work_dir,
                    file_type=file_type,
                    ignore_hidden_files=ignore_hidden_files,
                    deep_start=deep_start,
                    deep_count=deep_count,
                    regex_flag=regex_flag,
                )
            elif value == "rename_files" or value == "r":
                if Path(work_dir).exists() == False:
                    print_e(
                        "工作目录不存在, 重命名文件失败, 请传入-d/--work-dir参数为工作目录"
                    )
                    return

                def should_rename_delegate(rename_map: dict[str, str]) -> bool:
                    if yes == True:
                        return True
                    print_w("是否重命名以上目录?")
                    should_mkdir = inputt(
                        "确定请输入Y, 输入其他为取消重命名命令. 请输入[Y/n]\n"
                    )
                    if should_mkdir == "Y":
                        return True
                    return False

                self.manager.rename_files(
                    work_dir=work_dir,
                    source_pattern=source_pattern,
                    replace=replace,
                    deep_start=deep_start,
                    deep_count=deep_count,
                    count=count,
                    file_type=file_type,
                    ignore_hidden_files=ignore_hidden_files,
                    should_rename_delegate=should_rename_delegate,
                )
            elif value == "search_clean" or value == "sc":
                if Path(work_dir).exists() == False:
                    print_e(
                        "工作目录不存在, 搜索文件失败, 请传入-d/--work-dir参数为工作目录"
                    )
                    return

                def should_delete_delegate(path_list: list[Path]) -> bool:
                    if yes == True:
                        return True
                    print_w("是否清理以上对象?")
                    should_mkdir = inputt(
                        "确定请输入Y, 输入其他为取消清理命令. 请输入[Y/n]\n"
                    )
                    if should_mkdir == "Y":
                        return True
                    return False

                self.manager.search_clean(
                    keyword=keyword,
                    work_dir=work_dir,
                    file_type=file_type,
                    ignore_hidden_files=ignore_hidden_files,
                    deep_start=deep_start,
                    deep_count=deep_count,
                    regex_flag=regex_flag,
                    should_delete_delegate=should_delete_delegate,
                )
            elif value == "clean" or value == "c":
                if Path(work_dir).exists() == False:
                    print_e(
                        "工作目录不存在, 搜索文件失败, 请传入-d/--work-dir参数为工作目录"
                    )
                    return

                def should_delete_delegate(path_list: list[Path]) -> bool:
                    if yes == True:
                        return True
                    print_w("是否清理以上对象?")
                    should_mkdir = inputt(
                        "确定请输入Y, 输入其他为取消清理命令. 请输入[Y/n]\n"
                    )
                    if should_mkdir == "Y":
                        return True
                    return False

                self.manager.rglob_clean(
                    keyword=rglob_keyword,
                    work_dir=work_dir,
                    file_type=file_type,
                    ignore_hidden_files=ignore_hidden_files,
                    should_delete_delegate=should_delete_delegate,
                )
