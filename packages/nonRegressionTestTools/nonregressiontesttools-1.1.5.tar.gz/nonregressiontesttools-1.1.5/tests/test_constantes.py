# !/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2017-07-19 17:22:57.246629"
__version__ = 1.0
# **************************************************
from nonRegressionTestTools import constantes as CST
import pytest

VERBOSITY = 1


def _test_constante_obj(REFS, className, verbosity=0):

    flags = className()
    for att in list(flags.__class__.__dict__.keys()):
        if att[0].isupper():
            assert(att in list(REFS.keys()))
            val = flags.__getattribute__(att)
            assert(val == REFS[att])
    flags_dict = flags.get_cst_dict()
    for k, val in flags_dict.items():
        assert(k in list(REFS.keys()))

        assert(val == REFS[k])
    for val in flags_dict.values():

        flag_name = flags.get_cst_name(val)
        assert(val == REFS[flag_name])
        msg = className.msg(val)
        if verbosity > 0:
            print(msg)
        assert(msg != "")

def test_Constantes():
    cst = CST.Constantes()
    ret = cst.get_cst_name("INEXISTING")
    assert (ret == None)
    string = "coucou"
    ret = cst.var_name_to_print(string)
    assert (string == ret)
    ret = cst.filter_pattern()
    assert(ret == "")

def test_Boolean():
    REFS = {"NRT_OK": 1,
            "NRT_KO": 0,
            }
    _test_constante_obj(REFS=REFS, className=CST.Boolean, verbosity=VERBOSITY)


def test_FileReadCat():
    REFS = {"NRT_CONSTRUCTION": -1,
            "NRT_NOMINAL": 0,
            "NRT_FAILED": 1,
            "NRT_OTHERS": 2,
            }
    _test_constante_obj(REFS=REFS, className=CST.FileReadCat, verbosity=VERBOSITY)


def test_FileWriteCat():
    REFS = {"NRT_CONSTRUCTION": -1,
            "NRT_NOMINAL": 0,
            "NRT_FAILED": 1,
            }
    _test_constante_obj(REFS=REFS, className=CST.FileWriteCat, verbosity=VERBOSITY)


def test_TestCategories():
    REFS = {"NRT_CAT_KO": 0,
            "NRT_CAT_OK": 1,
            "NRT_CAT_OK_WARNING": 2,
            "NRT_CAT_CONSTRUCTION": 3,
            }
    _test_constante_obj(REFS=REFS, className=CST.TestCategories, verbosity=VERBOSITY)


def test_flags():
    REFS = {"NRT_FLAG_OK": 0,
            "NRT_FLAG_NO_RES": -1,
            "NRT_FLAG_NO_REF": -2,
            "NRT_FLAG_NO_READABLE_REF": -3,
            "NRT_FLAG_NO_READABLE_RES": -4,
            "NRT_FLAG_DOWNGRADED": -5,
            "NRT_FLAG_FIXED": -6,
            "NRT_FLAG_OK_WARNING": -7,
            "NRT_FLAG_UNDEFINED": -8,
            "NRT_FLAG_IGNORE": -999,
            "NRT_FLAG_CONSTRUCTION": 999,
            }
    _test_constante_obj(REFS=REFS, className=CST.Flags, verbosity=VERBOSITY)
    var = CST.Flags.var_name_to_print("NRT_FLAG_OK")
    print(var)
    assert(var == "OK")


def test_printObj():
    print("\nBoolean:")
    print(CST.Boolean())
    print("\nFileReadCat:")
    print(CST.FileReadCat())
    print("\nFileWriteCat:")
    print(CST.FileWriteCat())
    print("TestCategories:")
    print(CST.TestCategories())
    print("Flags:")
    print(CST.Flags())
