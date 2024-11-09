#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-09-28 09:35:57.986580"
__version__ = 1.0
# **************************************************
from nonRegressionTestTools import config
import os
os.environ['NRT_COLOR_MODE'] = "3"
os.environ['NRT_VERBOSITY_LEVEL'] = "10"
import pytest

def test_verbosity():
    verb = config.VerbosityManager()
    assert("verbosity" in list(verb.__class__.__dict__.keys()))
    assert(type(verb.verbosity) == int)
    assert(verb.verbosity == 3)
    verb.verbosity = 4
    assert(verb.verbosity == 4)


def test_NRT_ENV_VARIABLES():
    conf = config.Config()
    print(conf)
    for k, val in conf.__dict__.items():
        if k.startswith("NRT_"):
            print(k,"->", val)

    config.conf.NRT_COLOR_MODE = 1
    color = config.get_color_fmt()

    config.conf.NRT_COLOR_MODE = 0
    color = config.get_color_fmt()

    # print(conf.NRT_RECIPE_EXT)
    # print(conf.NRT_RESULT_EXT)
    # print(conf.NRT_STATE_EXT)
    # print(conf.NRT_DIR_RESULTS)
    # print(conf.NRT_COLOR_MODE)
    # print(conf.NRT_VERBOSITY_LEVEL)

    # print(os.getenv("NRT_RECIPE_EXT"))
    # print(os.getenv("NRT_RESULT_EXT"))
    # print(os.getenv("NRT_STATE_EXT"))
    # print(os.getenv("NRT_COLOR_MODE"))
    # print(os.getenv("NRT_VERBOSITY_LEVEL"))
