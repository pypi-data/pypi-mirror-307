#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-04-30 09:33:24.135766"
__version__ = 1.0
# **************************************************
from . import constantes as CST

class iTestFilter():
    implemented_filters = {}

    def __init__(self, initial_list:list=[]):
        self.test_lst = initial_list.copy()
        self.lst = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        key = str(cls.__name__.replace("Test", "").replace("Filter", ""))
        cls.implemented_filters[key] = cls

    def _apply(self):
        raise NotImplementedError("Must be override")  #pragma: no cover

    def apply(self):
        self._apply()
        return self.lst

class RegexTestFilter(iTestFilter):

    def __init__(self, regex:str="", **kwd):
        super().__init__(**kwd)
        self.regex=regex
    def _apply(self):
        self.lst =[]
        for test in self.test_lst:
            if self.regex in test.directory:
                self.lst.append(test)
        return


def classBuilder(clsName, cond):
    cname = clsName+"TestFilter"
    assert(cname not in iTestFilter.implemented_filters.keys())
    def _apply(self):
        self.lst = []
        for test in self.test_lst:
            flags = test.flags
            if cond in flags:
                self.lst.append(test)
        return

    newclass = type(cname, (iTestFilter,), {"_apply":  lambda self: _apply(self)})
    return cname


def defineFilters():
    # ALL = dir(CST.Flags)
    # STATUS = []
    # for i in  ALL:
    #     if i.startswith("STAT_"):
    #         STATUS.append(i.replace("STAT_","").lower())
    # STATUS.remove("IGNORE")
    FLAGS = list(CST.Flags.get_cst_dict().keys())
    for flag in FLAGS:
        cond = CST.Flags.__dict__[flag]
        classBuilder(flag, cond)
    return

defineFilters()
