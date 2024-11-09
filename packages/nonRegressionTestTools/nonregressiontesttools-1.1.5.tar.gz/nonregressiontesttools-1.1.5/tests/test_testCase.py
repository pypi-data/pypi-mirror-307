#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-10-14 09:24:24.400699"
__version__ = 1.0
# **************************************************
from nonRegressionTestTools import constantes as CST
from nonRegressionTestTools import testCase as TC
from nonRegressionTestTools import config as CONF
import os

import pytest

VERBOSITY = 1

def test_TestCaseStructure():
    test_directory = "/path/to/testBase"
    test_name = "testName"
    recipe = os.path.join(test_directory, test_name + CONF.conf.NRT_RECIPE_EXT)
    res_dir = os.path.join(test_directory, CONF.conf.NRT_DIR_RESULTS)
    res = os.path.join(res_dir, test_name + CONF.conf.NRT_RESULT_EXT)
    state = os.path.join(res_dir, test_name + CONF.conf.NRT_STATE_EXT)
    tcs1 = TC.TestCaseStructure(test_dir=test_directory,
                               test_name=test_name)
    assert(tcs1.name == test_name)
    assert(tcs1.directory== test_directory)
    assert(tcs1.recipe == recipe)
    assert(tcs1.res_dir == res_dir)
    assert(tcs1.res == res)
    assert(tcs1.state == state)
    if VERBOSITY:
        print(tcs1)
        to_print = tcs1.__repr__().replace(test_directory, ".")
        print(to_print)

    tcs2 = TC.TestCaseStructure.from_recipe(recipe, CONF.conf.NRT_RECIPE_EXT)
    assert(tcs1 == tcs2)
    return

def test_TestCase():
    recipe =  os.path.join(os.path.dirname(__file__), "01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/00-TEST-ALWAYS-OK", "runme"+CONF.conf.NRT_RECIPE_EXT)
    tc = TC.TestCase(recipe=recipe)
    print(tc.ref_statu)
    print(tc.last_run_statu)
    print(CST.TestCategories.get_cst_pname(tc.category))
    print(tc.filename)
    print(tc.statu)
    print(tc)
    assert(tc.statu == True)
    recipe =  os.path.join(os.path.dirname(__file__), "01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/01-TEST-WITHOUT-RES", "runme"+CONF.conf.NRT_RECIPE_EXT)
    tc = TC.TestCase(recipe=recipe)
    print(tc)
    assert(tc.statu == False)
    return

# test_TestCaseStructure()
