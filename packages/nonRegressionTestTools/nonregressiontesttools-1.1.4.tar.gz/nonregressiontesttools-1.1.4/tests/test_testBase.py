# !/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2017-07-19 17:22:57.246629"
__version__ = 1.0
# **************************************************
import os
import sys
from nonRegressionTestTools import genericTestBase as GTB
from nonRegressionTestTools import config as CONF


VERBOSITY = 1
NRT_RECIPE_EXT = CONF.conf.NRT_RECIPE_EXT

def test_testBase():
    PATH = os.path.join(os.path.dirname(__file__), "01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/00-TEST-ALWAYS-OK")
    test_cases = GTB.test_cases(path=PATH,
                                ext=NRT_RECIPE_EXT,
                                verbosity_level=1)
    assert(test_cases.statu==True)

    PATH = os.path.join(os.path.dirname(__file__), "01-TEST-BASE-EXAMPLES/01-CHECK-STATUS")
    test_cases = GTB.test_cases(path=PATH,
                                ext=NRT_RECIPE_EXT,
                                verbosity_level=1)

    assert(test_cases.statu==False)
