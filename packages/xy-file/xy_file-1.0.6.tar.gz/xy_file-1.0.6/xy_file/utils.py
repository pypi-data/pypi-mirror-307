# -*- coding: UTF-8 -*-
__author__ = "余洋"
__doc__ = "utils"
"""
  * @File    :   utils.py
  * @Time    :   2023/06/03 22:23:42
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyangit.0515@qq.com
  * @License :   (C)Copyright 2019-2024, 希洋 (Ship of Ocean)
  * @Desc    :   None
"""

from rich.console import Console

xy_c = Console()
xy_p = xy_c.print

_success = "bold #22ff00"
_execute = "bold #00ffff"
_warning = "bold #ffff00"
_run = "bold #2266ff"
_error = "bold #ff4500"
_red = "bold red"
_green = "bold green"
_blue = "bold blue"
_seperate_text = "\n======================================\n"


def inputt(
    text: str,
    prefix=_seperate_text,
    markup: bool = True,
    emoji: bool = True,
    password: bool = False,
    stream=None,
    *args,
    **kwargs,
):
    return xy_c.input(
        f"{prefix}{text}",
        markup=markup,
        emoji=emoji,
        password=password,
        stream=stream,
        *args,
        **kwargs,
    )


def printt(
    text: str,
    style: str = _run,
    prefix=_seperate_text,
    sep: str = " ",
    end: str = "\n",
    new_line_start: bool = False,
    crop: bool = True,
    justify=None,
    overflow=None,
    no_wrap=None,
    emoji=None,
    markup=None,
    highlight=None,
    width=None,
    height=None,
    soft_wrap=None,
) -> None:
    xy_p(
        f"{prefix}{text}",
        style=style,
        sep=sep,
        end=end,
        new_line_start=new_line_start,
        crop=crop,
        justify=justify,
        overflow=overflow,
        no_wrap=no_wrap,
        emoji=emoji,
        markup=markup,
        highlight=highlight,
        width=width,
        height=height,
        soft_wrap=soft_wrap,
    )


def print_s(
    text: str,
    prefix=_seperate_text,
):
    printt(
        text=text,
        prefix=prefix,
        style=_success,
    )


def print_exe(
    text: str,
    prefix=_seperate_text,
):
    printt(
        text=text,
        prefix=prefix,
        style=_execute,
    )


def print_w(
    text: str,
    prefix=_seperate_text,
):
    printt(
        text=text,
        prefix=prefix,
        style=_warning,
    )


def print_r(
    text: str,
    prefix=_seperate_text,
):
    printt(
        text=text,
        prefix=prefix,
        style=_run,
    )


def print_e(
    text: str,
    prefix=_seperate_text,
):
    printt(
        text=text,
        prefix=prefix,
        style=_error,
    )
