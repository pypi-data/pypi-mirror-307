#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-04-26 14:00:51.591452"
__version__ = 1.0
# **************************************************
from . import config as CONF


class Constantes():

    @classmethod
    def get_cst_dict(cls):
        to_ret = {}
        for att in list(cls.__dict__.keys()):
            if att.isupper():
                to_ret[att] = cls.__getattribute__(cls, att)
        return to_ret

    @classmethod
    def get_cst_name(cls, cat_num:int):
        cats = cls.get_cst_dict()
        keys = list(cats.keys())
        val = list(cats.values())
        inv_dict = dict(zip(val, keys))
        if cat_num in list(inv_dict.keys()):
            to_ret = inv_dict[cat_num]
            return to_ret
        else:
            return None

    @classmethod
    def get_cst_pname(cls, cat_num:int):
        color_dic = CONF.get_color_fmt().__dict__
        to_ret = cls.get_cst_name(cat_num)
        if to_ret in list(color_dic.keys()):
            to_ret = color_dic[to_ret]+to_ret+color_dic["END"]
        return to_ret

    @classmethod
    def var_name_to_print(cls, var_name):
        return var_name

    @classmethod
    def msg(cls, val):
        Color = CONF.get_color_fmt()
        assert(val in list(cls.get_cst_dict().values()))
        var_name = cls.get_cst_name(val)
        name = cls.var_name_to_print(var_name)
        return Color.__dict__[var_name] + name + Color.END

    def __setattr__(self, name, value):
        return

    def filter_pattern(self):
        return ""

    def __repr__(self):
        color_dic = CONF.get_color_fmt().__dict__
        to_ret = ""
        for k, val in self.__class__.__dict__.items():
            if k.startswith(self.filter_pattern()):
                if k in list(color_dic.keys()):
                    to_ret += "{}{}{}: {}\n".format(color_dic[k],
                                                    self.__class__.var_name_to_print(k),
                                                    color_dic["END"],
                                                    val)
                else:
                    to_ret += "{}: {}\n".format(k, val)
        return to_ret

    def __str__(self):
        return self.__repr__()



class NRT_Constantes(Constantes):

    def filter_pattern(self):
        return "NRT_"

    @classmethod
    def var_name_to_print(cls, var_name):
        name = var_name
        if var_name.startswith("NRT_"):
            name = var_name.split("NRT_")[-1]
        return name


class Boolean(NRT_Constantes):
    NRT_KO = 0
    NRT_OK = 1


class FileReadCat(NRT_Constantes):
    NRT_CONSTRUCTION = -1
    NRT_NOMINAL = 0
    NRT_FAILED = 1
    NRT_OTHERS = 2


class FileWriteCat(NRT_Constantes):
    NRT_CONSTRUCTION = -1       # specific output to flag the test as in CONSTRUCTION
    NRT_NOMINAL = 0             # nominal output
    NRT_FAILED = 1              # output if something goes wrong


class TestCategories(Boolean, NRT_Constantes):
    NRT_CAT_KO = 0                # not in all other categorie
    NRT_CAT_OK = 1                # if .res and .state has the same flag OK
    NRT_CAT_OK_WARNING = 2        # if .res and .state has the same flag  but flag is different than OK
    NRT_CAT_CONSTRUCTION = 3      # if .res or .state has the flag CONSTRUCTION

    @classmethod
    def var_name_to_print(cls, var_name):
        name = var_name
        if var_name.startswith("NRT_CAT_"):
            name = var_name.split("NRT_CAT_")[-1]
        return name


class Flags(Constantes):
    NRT_FLAG_OK = 0                # test case is ok if .res and .state has this flag
    NRT_FLAG_NO_RES = -1           # .res is missing
    NRT_FLAG_NO_REF = -2           # .state is missing
    NRT_FLAG_NO_READABLE_REF = -3  # .res is not readable (file exist)
    NRT_FLAG_NO_READABLE_RES = -4  # .state is not readable (file exist)
    NRT_FLAG_DOWNGRADED = -5       # .res is different thant .state and .state has the flag OK
    NRT_FLAG_FIXED = -6            # .res flag turn to OK
    NRT_FLAG_OK_WARNING = -7       # .res's flag egal .state's flag but the falg is different than OK
    NRT_FLAG_UNDEFINED = -8        # .res's flag is different than .state's flag and none of them has OK flag
    NRT_FLAG_CONSTRUCTION = 999    # specifig flag to declare in .state (recommanded at least) or .res that the test is under construction
    NRT_FLAG_IGNORE = -999         # ignore the test from the test base
    # DOC END Flags             do not remove this comment that is usefful for the doc

    @classmethod
    def msg(cls, statu):
        Color = CONF.get_color_fmt()
        assert(statu in list(cls.get_cst_dict().values()))
        if statu is Flags.NRT_FLAG_OK:
            return "Reference and result status match"
        if statu is Flags.NRT_FLAG_NO_REF:
            return "Reference statu is missing"
        if statu is Flags.NRT_FLAG_NO_RES:
            return "Result statu is missing"
        if statu is Flags.NRT_FLAG_NO_READABLE_REF:
            return "Reference statu format is not as expected (int)"
        if statu is Flags.NRT_FLAG_NO_READABLE_RES:
            return "Reference result format is not as expected (int)"
        if statu is Flags.NRT_FLAG_DOWNGRADED:
            return Color.NRT_KO+"↓"+Color.END+" Last job produce an unexpected results"
        if statu is Flags.NRT_FLAG_FIXED:
            return Color.NRT_OK+"↑"+Color.END+" Reference state should be updated"
        if statu is Flags.NRT_FLAG_OK_WARNING:
            return "Statu are the same but its value is not nominal"
        if statu is Flags.NRT_FLAG_UNDEFINED:
            return "Reference statu and results statu differs and none of them are nominal"
        if statu is Flags.NRT_FLAG_IGNORE:
            return "Ignore test"
        if statu is Flags.NRT_FLAG_CONSTRUCTION:
            return "Test in construction"
        return ""  #pragma: no cover

    @classmethod
    def var_name_to_print(cls, var_name):
        name = var_name
        if var_name.startswith("NRT_"):
            name = var_name.split("NRT_FLAG_")[-1]
        return name

    def filter_pattern(self):
        return "NRT_FLAG_"

    def __init__(self, *args, **kwd):
        self.res_val = 0
        self.ref_val = 0
        self.stderr = ""
        self.msg = ""



class ColorActivated():
    FLAG = "\033[38;5;03m"
    END = "\033[0m"
    SUMMARY = "\033[38;5;04m"
    CONSTRUCTION = "\033[38;5;04m"

    # TestCategories
    NRT_CAT_KO = "\033[38;5;196m"
    NRT_CAT_OK = "\033[38;5;040m"
    NRT_CAT_OK_WARNING = "\033[38;5;202m"
    NRT_CAT_CONSTRUCTION = "\033[38;5;04m"

    # FileWriteCat
    NRT_NOMINAL = "\033[48;5;255m\033[38;5;040m"
    NRT_FAILED = "\033[48;5;255m\033[38;5;196m"
    NRT_CONSTRUCTION = "\033[48;5;255m\033[38;5;04m"

    # BOOLEAN STATUS
    NRT_KO = "\033[38;5;196m"
    NRT_OK = "\033[38;5;040m"
    NRT_OTHERS = "\033[48;5;255m\033[38;5;202m"

    NRT_MISSING = "\033[01;5;03m"

    NRT_FLAG___OK = "✅"
    NRT_FLAG___KO = "❌"


class ColorRemove:
    FLAG = ""
    END = ""
    SUMMARY = ""
    BUILD = ""

    # TestCategories
    NRT_CAT_KO = ""
    NRT_CAT_OK = ""
    NRT_CAT_OK_WARNING = ""
    NRT_CAT_CONSTRUCTION = ""

    # FileWriteCat
    NRT_NOMINAL = ""
    NRT_FAILED = ""
    NRT_CONSTRUCTION = ""

    # BOOLEAN STATUS
    NRT_KO = ""
    NRT_OK = ""
    NRT_OTHERS = ""

    NRT_MISSING =  ""

    NRT_FLAG___OK = "✅"
    NRT_FLAG___KO = "❌"
