#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 21:52
# @Author  : 兵
# @email    : 1747193328@qq.com
import os

from NepTrain import Config
from NepTrain import utils


def check_env():
    if not os.path.exists(os.path.expanduser(Config.get("environ", "potcar_path"))):
        raise FileNotFoundError("请编辑~/.NepTrain设置有效的赝势文件路径！")

    for option in ["vasp_path", "mpirun_path", "nep_path", "gpumd_path"]:
        if utils.get_command_result(["which", Config.get("environ", option)]) is None:
            utils.print_warning(f"环境变量中没有{option.replace('_path', '')},如果在提交脚本里设置环境，请忽略这条警告")

