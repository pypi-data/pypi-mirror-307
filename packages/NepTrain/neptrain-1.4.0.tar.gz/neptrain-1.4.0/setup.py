#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 14:22
# @Author  : 兵
# @email    : 1747193328@qq.com
"""Pymatgen package configuration."""

from __future__ import annotations

import platform
import sys

import numpy as np
from setuptools import Extension, setup

is_win_64 = sys.platform.startswith("win") and platform.machine().endswith("64")
extra_link_args = ["-Wl,--allow-multiple-definition"] if is_win_64 else []

setup(
    author="Chen Cheng bing",

    include_dirs=[np.get_include()],
)