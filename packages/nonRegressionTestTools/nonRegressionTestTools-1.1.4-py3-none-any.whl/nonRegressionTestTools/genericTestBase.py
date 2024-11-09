# !/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2017-07-19 17:22:57.246629"
__version__ = 1.0
# **************************************************


# ////////////////////////////////////////////////////////////////////////////////////////////////////
#                    BEGINING OF THE CODE
# ////////////////////////////////////////////////////////////////////////////////////////////////////
from . import constantes as CST
from . import runners as RUN
from . import statutsManager as StatM
from . import filters
from . import testCase
import os
import numpy as np
from . import config as CONF


class test_cases(CONF.VerbosityManager):
    """
    This is the object test base which contain all test_case object and some usefull fonctions to act on them
    """

    def __init__(self, path:str=os.getcwd(),
                 recursive:bool=True,
                 filter_name:str="",
                 regex:str="",
                 ext=CONF.conf.NRT_RECIPE_EXT, **kwd):
        super().__init__(**kwd)
        self.path = path
        self.recursive = recursive
        self.filter_name = filter_name
        self.regex=regex
        self.testCases = []
        self.ext = ext
        self._find_test_cases()
        self._filters = []
        self._set_filters()
        self._apply_filters()
        self._sort()
        self.all_test_OK = False
        return

    def _find_test_cases(self):
        """
        return findf *.ext, path, results
        where ext is .recipe by default
        """
        for root, subFolder, files in os.walk(self.path):
            for ifile in files:
                splitfile = os.path.splitext(ifile)
                if splitfile[1] == self.ext:
                    recipe = os.path.join(root, ifile)
                    self.testCases.append(testCase.TestCase(recipe=recipe,
                                                            cwd=self.path,
                                                            verbosity_level=self.verbosity))
            if not self.recursive:
                break
        return

    def _sort(self):
        dirs = [test.abs_dir for test in self.testCases]
        idx = list(zip(dirs, range(len(dirs))))
        # sort by directory name
        cas = {}
        for k in idx:
            if k[0] in list(cas.keys()):
                cas[k[0]].append(k[1])
            else:
                cas[k[0]] = [k[1]]
        dirs = np.unique(dirs)
        dirs.sort()
        # sort by filname in directory
        new_order = []
        for idir in dirs:
            names = [self.testCases[i].filename for i in cas[idir]]
            idx2 = dict(zip(names, range(len(names))))
            names.sort()
            new_idx = []
            for name in names:
                new_idx.append(idx2[name])
            new_order += list(np.array(cas[idir])[new_idx])
        self.testCases = [self.testCases[i] for i in new_order]
        return


    def _set_filters(self):
        allow_filters = filters.iTestFilter.implemented_filters
        if self.filter_name in allow_filters.keys():
            if self.filter_name == "Regex":
                pass   #pragma: no cover
            else:
                ifilter = allow_filters[self.filter_name](initial_list=self.testCases)
                self._filters.append(ifilter)
        else:
            if self.filter_name == "":
                pass
            else:   #pragma: no cover
                raise NotImplementedError("\n Filter \"{}\" is not allowed\n Candidates are {}".format(self.filter_name, ", ".join(list(allow_filters.keys()))))
        if self.regex != "":
                ifilter = allow_filters["Regex"](initial_list=self.testCases,regex=self.regex)
                self._filters.append(ifilter)

        return

    def _apply_filters(self):
        for ifilter in self._filters:
            self.testCases = ifilter.apply()
            self.testCases = ifilter.lst
        if self.verbosity > 1:
            print("filter applied")
        return


    def run(self, *args, **kwd):
        """
        run all the selected tests
        options:
        -b to run only the broken tests
        -c to run only the broken tests
        """
        for icase in self.testCases:
            iProc = icase.run()
        # self.print_bilan( *args, **kwd)
        return

    def print_stats(self, *args,  **kwd):
        """
        print stats messages
        """
        Color = CONF.get_color_fmt()
        cats = []
        for icase in self.testCases:
            cats.append(icase.category)

        ct_tests = len(self.testCases)
        cats = np.array(cats, dtype=np.int32).reshape(-1)
        ct_ok = np.argwhere(cats == CST.TestCategories.NRT_CAT_OK).shape[0]
        ct_build = np.argwhere(cats == CST.TestCategories.NRT_CAT_CONSTRUCTION).shape[0]
        to_print = ""
        if ct_tests > 0:
            ratio = ct_ok/ct_tests*100
            ct_failed = ct_tests-ct_ok-ct_build
            to_print = "\n"+Color.SUMMARY+"-"*50+Color.END
            to_print += "\nSummary : |"+Color.NRT_CAT_OK+"{:2.1f}% OK ({}/{})".format(ratio, ct_ok,ct_tests)+Color.END+" |"
            to_print += Color.NRT_CAT_KO+"{:2.1f}% KO ({}/{})".format(ct_failed/ct_tests*100,ct_failed,ct_tests,)+Color.END+"| "
            to_print += Color.NRT_CAT_CONSTRUCTION+"{:2.1f}% IN CONSTRUCTION ({}/{})".format(ct_build/ct_tests*100,ct_build,ct_tests,)+Color.END+"| "
            to_print += "\n"+Color.SUMMARY+"-"*50+Color.END
            if ct_tests == ct_ok:
                self.all_test_OK = True
        else:
            to_print = "0 test run"
            self.all_test_OK = True
        print(to_print)
        return

    def print_tests_to_fix(self, *args,  **kwd):
        """
        print all tests to fix.
        """
        Color = CONF.get_color_fmt()
        print("\n"+Color.FLAG+"-"*15+"TESTS WITH NO NOMINAL FLAG"+"-"*20+Color.END)
        statuts = []
        for icase in self.testCases:
            icase.flags_msg()
        print(Color.FLAG+"-"*50+Color.END)
        return

    def print_bilan(self, quiet:bool=False, *args,  **kwd):
        """
        print bilan messages
        """
        print("-"*50)
        print(" "*25+"Bilan (verbosity: {})".format(self.verbosity)+" "*25)
        print("-"*50)
        if self.verbosity > 0:
            print(self.testCases)
        else:
            for icase in self.testCases:
                icase.bilan()
        self.print_stats()
        if not quiet:
            if not self.all_test_OK:
                self.print_tests_to_fix()
        print("-"*50)
        return

    def flags(self, *args, **kwd):
        """
        run all the selected tests
        options:
        -b to run only the broken tests
        -c to run only the broken tests
        """
        all_flags = {}
        for icase in self.testCases:
            flags = icase.flags
            all_flags[os.path.join(icase.directory, icase.filename)] = flags
        # self.print_bilan( *args, **kwd)
        return all_flags

    @property
    def statu(self):
        satus = []
        for icase in self.testCases:
            stat = icase.statu
            if not stat:
                return False
        return True

    def __repr__(self):
        to_return = ""
        for icase in self.testCases:
            to_return += "-"*50+"\n"
            to_return += icase.__repr__()
            to_return += "-"*50+"\n"
            to_return += "\n"
        return to_return
# --------------------------------------------------
