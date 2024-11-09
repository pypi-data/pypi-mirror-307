#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-10-14 08:58:19.561909"
__version__ = 1.0
# **************************************************


# ////////////////////////////////////////////////////////////////////////////////////////////////////
#                    BEGINING OF THE CODE
# ////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////
#                    BEGINING OF THE CODE
# ////////////////////////////////////////////////////////////////////////////////////////////////////
from . import constantes as CST
from . import runners as RUN
from . import statutsManager as StatM
from . import filters
from . import config
import os
from . import config as CONF



class TestCaseStructure(CONF.VerbosityManager):
    """
    Describe the structure of a test case
    default:
    .
    | - foo.recipe
          |- .test_results
              |- foo.res
              |- foo.stat


    """
    @classmethod
    def from_recipe(cls, recipeFilePath:str, recipe_ext:str='.recipe'):
        recipeFile = os.path.basename(recipeFilePath)
        test_dir = os.path.dirname(recipeFilePath)
        splitFile = os.path.splitext(recipeFile)
        test_name = splitFile[0]
        recipe_ext = splitFile[1]
        if recipe_ext != recipe_ext: # pragma: no cover
            raise RuntimeError("file {} does not look like a recipe file\n\
            its extension is {} while the expected one is {}\
            ".format(recipeFile, recipe_ext, recipe_ext))
        return TestCaseStructure(test_dir=test_dir,
                                 test_name=test_name)


    def __init__(self, test_dir:str="/tmp", test_name:str="test_case", **kwd):
        self._name = test_name
        self._directory = test_dir
        self._res_dir = None    # set by initialSetup
        self._res_file = None        # set by initialSetup
        self._state_file = None      # set by initialSetup
        self._recipe = None     # set by initialSetup
        self._initialSetup()

    def _initialSetup(self):
        self._set_recipe_file()       # set PATH/.results
        self._set_res_dir()       # set PATH/.results
        self._set_res_file()       # set PATH/.results/foo.res
        self._set_state_file()  # set PATH/.results/foo.state

    def _set_recipe_file(self):
        self._recipe = os.path.join(self.directory,
                                    self.name+ CONF.conf.NRT_RECIPE_EXT)
        return

    def _set_res_dir(self):
        self._res_dir = os.path.join(self.directory,
                                     CONF.conf.NRT_DIR_RESULTS)
        return

    def _set_res_file(self):
        """
        set PATH_TO/.results/foo.res
        """
        fn = self.name+CONF.conf.NRT_RESULT_EXT
        self._res_file = os.path.join(self.res_dir,
                                           fn)
        return

    def _set_state_file(self):
        """
        set PATH_TO/.results/foo.state
        """
        fn = self.name+CONF.conf.NRT_STATE_EXT
        self._state_file = os.path.join(self._res_dir,
                                        fn)
        return

    @property
    def directory(self):
        return self._directory

    @property
    def name(self):
        return self._name

    @property
    def recipe(self):
        return self._recipe

    @property
    def res_dir(self):
        return self._res_dir

    @property
    def res(self):
        return self._res_file

    @property
    def state(self):
        return self._state_file

    def  __repr__(self):
        to_ret = ""
        to_ret += "test structure:\n"
        to_ret += "- recipe ({}):\n  {}\n".format(CONF.conf.NRT_RECIPE_EXT, self.recipe)
        to_ret += "   - results directory ({}):\n     {}\n".format(CONF.conf.NRT_DIR_RESULTS, self.res_dir)
        to_ret += "        - state file ({}):\n          {}\n".format(CONF.conf.NRT_STATE_EXT, self.state)
        to_ret += "        - last run file ({}):\n          {}\n".format(CONF.conf.NRT_RESULT_EXT, self.res)
        return to_ret

    def __eq__(self, obj):
        if not isinstance(obj, self.__class__):  # pragma: no cover
            return False
        else:
            return self.recipe == obj.recipe and self.res_dir == obj.res_dir and self.state == obj.state and self.res == obj.res



class TestCase(CONF.VerbosityManager):
    """
    This is the test case object
    """
    def __init__(self, recipe:str, cwd:str=None,**kwd):
        super().__init__(**kwd)
        self._recipeFile = recipe
        self._cwd = cwd
        self.recipe = StatM.FileInfo(fn=self._recipeFile, cwd=self._cwd)
        if not self.recipe.valid:   # pragma: no cover
            raise RuntimeError("Can't create a test with the recipe {}".format(self.recipe.fn))
        self.struct = TestCaseStructure.from_recipe(self.recipe.fn, CONF.conf.NRT_RECIPE_EXT)
        self._initial_process()
        return

    def _initial_process(self):
        self._set_runner()
        return

    @property
    def ref_statu(self):
        """
        return statu of .state
        """
        return StatM.FileStatu.get(self.struct.state)

    @property
    def last_run_statu(self):
        """
        return statu of .res
        """
        return StatM.FileStatu.get(self.struct.res)


    @property
    def category(self):
        """
        return the category of the test.
        see CST.TestCategories.get_cst_dict()
        """
        refStat = self.ref_statu
        lruStat = self.last_run_statu
        cat = CST.TestCategories.NRT_CAT_KO

        if lruStat == refStat:
            if (refStat.valueCat == CST.FileReadCat.NRT_NOMINAL):
                cat = CST.TestCategories.NRT_CAT_OK
            elif (refStat.valueCat == CST.FileReadCat.NRT_FAILED):
                cat = CST.TestCategories.NRT_CAT_KO
            elif (refStat.valueCat == CST.FileReadCat.NRT_OTHERS and refStat.valueValid):
                cat = CST.TestCategories.NRT_CAT_OK_WARNING
        else:
            if (refStat.valueCat == CST.FileReadCat.NRT_CONSTRUCTION) or (lruStat.valueCat == CST.FileReadCat.NRT_CONSTRUCTION):
                cat = CST.TestCategories.NRT_CAT_CONSTRUCTION
            else:
                cat = CST.TestCategories.NRT_CAT_KO
        return cat


    def _set_runner(self):
        self._runner = RUN.BashRunner(cmd_file=self.recipe.fn,
                                      abs_dir=self.struct.directory,
                                      verbosity_level=self.verbosity)
        return

    @property
    def abs_dir(self):
        """
        return the abolute path to the directory where the test is.
        """
        return self.struct.directory

    @property
    def directory(self):
        """
        return the directory where the test is.
        it can be the absolute or relative path .
        """
        if self._cwd is None:   #pragma: no cover
            return self.recipe.fDirPath
        else:
            if self.recipe.rDirPath:
                return self.recipe.rDirPath
            else:               #pragma: no cover
                return self.recipe.fDirPath
        return

    @property
    def filename(self):
        """
        return the filename of the receipy to run the test
        """
        return self.struct.recipe

    def run(self):
        """
        run the test
        """
        self._runner.run()
        self.bilan()
        return

    def _flags_to_print(self):
        Color = CONF.get_color_fmt()
        to_print = "\n\t|"
        for flag in self.flags:
            to_print += Color.FLAG+CST.Flags.var_name_to_print(CST.Flags.get_cst_name(flag))+ Color.END + "|"
        return to_print

    def _flags_verbose_header(self):
        refStat = self.ref_statu
        lruStat = self.last_run_statu
        Color = CONF.get_color_fmt()
        to_print = ""
        to_print = " "+ CST.TestCategories.get_cst_pname(self.category).replace("NRT_CAT_", "")
        to_print += " -- " + self.directory + " " + self.recipe.name.rstrip()
        to_print += self._flags_to_print()
        return to_print


    def _flags_verbose(self):
        Color = CONF.get_color_fmt()
        refStat = self.ref_statu
        lruStat = self.last_run_statu
        to_print = self._flags_verbose_header()
        msg_added = False
        to_print += "\n"
        to_add = ""
        for flag in self.flags:
            to_print += "\t-> "+str(CST.Flags.msg(flag))+"\n"
            if (flag is CST.Flags.NRT_FLAG_DOWNGRADED)\
               or (flag is CST.Flags.NRT_FLAG_FIXED)\
               or (flag is CST.Flags.NRT_FLAG_OK_WARNING)\
               or (flag is CST.Flags.NRT_FLAG_UNDEFINED):
                if not msg_added:
                    if refStat.valueValid:
                        _cat = CST.FileReadCat.get_cst_pname(refStat.valueCat).replace("NRT_","")
                        to_add += "\t-- ref value: "+_cat+" ({})".format(refStat.value)+"\n"
                    if lruStat.valueValid:
                        _cat = CST.FileReadCat.get_cst_pname(lruStat.valueCat).replace("NRT_","")
                        to_add += "\t-- res value: "+_cat+" ({})".format(lruStat.value)+"\n"
                    msg_added = True
        to_print +=  to_add+"\n"
        return to_print

    def _flags_verbose1(self):
        Color = CONF.get_color_fmt()
        to_print = self._flags_verbose_header()
        to_print += "\n"
        to_print += "\t {}\n".format(self.struct.state.replace(self.struct.directory, "."))
        if self.ref_statu.openStat and self.ref_statu.readStatu:
            to_print += "\tcategory: {}\n\tvalue: {}\n".format(CST.FileReadCat.get_cst_pname( self.ref_statu.valueCat),
                                                      self.ref_statu.value )
        else:
            to_print += "\t"+CONF.get_color_fmt().NRT_MISSING+"MISSING"+CONF.get_color_fmt().END+"\n"
        to_print += "\t {}\n".format(self.struct.res.replace(self.struct.directory, "."))
        if self.last_run_statu.openStat and self.last_run_statu.readStatu:
            to_print +="\tcategory: {}\n\tvalue: {}\n".format(CST.FileReadCat.get_cst_pname( self.last_run_statu.valueCat),
                                                         self.last_run_statu.value)
        else:
            to_print += "\t"+CONF.get_color_fmt().NRT_MISSING+"MISSING"+CONF.get_color_fmt().END+"\n"
        return to_print


    def _flags_verbose2(self):
        Color = CONF.get_color_fmt()
        to_print = self._flags_verbose_header()
        to_print += "\n"
        to_print += self.ref_statu.__repr__().replace("NRT_", "")
        if not (self.ref_statu.openStat and self.ref_statu.readStatu):
            to_print += "\t"+CONF.get_color_fmt().NRT_MISSING+"MISSING"+CONF.get_color_fmt().END+"\n"
        to_print += self.last_run_statu .__repr__().replace("NRT_", "")
        if not (self.last_run_statu.openStat and self.last_run_statu.readStatu):
            to_print += "\t"+CONF.get_color_fmt().NRT_MISSING+"MISSING"+CONF.get_color_fmt().END+"\n"
        return to_print


    def flags_msg(self):
        """
        return the printable flags raised by the test.
        """
        to_print = ""
        if self.category != CST.TestCategories.NRT_CAT_OK:
            fverbos = None
            if self.verbosity == 0:
                fverbos =  self._flags_verbose
            if self.verbosity == 1:
                fverbos =  self._flags_verbose1
            if self.verbosity > 1:
                fverbos = self._flags_verbose2
            to_print += fverbos()
            print(to_print)
        else:
            pass
        return

    @property
    def flags(self):
        refStat = self.ref_statu
        lruStat = self.last_run_statu

        to_return = []

        if (self.category == CST.TestCategories.NRT_CAT_OK):
            to_return.append(CST.Flags.NRT_FLAG_OK)
        else:
            if not refStat.openStat:
                to_return.append(CST.Flags.NRT_FLAG_NO_REF)
            else:
                if not refStat.readStatu:  # pragma: no cover
                    to_return.append(CST.Flags.NRT_FLAG_NO_READABLE_REF)
                else:
                    if not refStat.valueValid:
                        to_return.append(CST.Flags.NRT_FLAG_NO_READABLE_REF)

            if not lruStat.openStat:
                to_return.append(CST.Flags.NRT_FLAG_NO_RES)
            else:
                if not lruStat.readStatu: # pragma: no cover
                    to_return.append(CST.Flags.NRT_FLAG_NO_READABLE_RES)
                else:
                    if not lruStat.valueValid:
                        to_return.append(CST.Flags.NRT_FLAG_NO_READABLE_RES)


        rcat = refStat.valueCat
        lcat = lruStat.valueCat

        if rcat != CST.FileReadCat.NRT_NOMINAL or lcat != CST.FileReadCat.NRT_NOMINAL:
            if rcat == CST.FileReadCat.NRT_NOMINAL:
                to_return.append(CST.Flags.NRT_FLAG_DOWNGRADED)

            if lcat == CST.FileReadCat.NRT_NOMINAL:
                to_return.append(CST.Flags.NRT_FLAG_FIXED)

            if refStat.valueValid and lruStat.valueValid:
                if refStat.value == lruStat.value and lruStat.value != CST.FileReadCat.NRT_OTHERS:
                    to_return.append(CST.Flags.NRT_FLAG_OK_WARNING)

                if rcat == CST.FileReadCat.NRT_OTHERS or lcat ==  CST.FileReadCat.NRT_OTHERS:
                    if refStat.value != lruStat.value:
                        to_return.append(CST.Flags.NRT_FLAG_UNDEFINED)
            else:
                pass

        if rcat == CST.FileReadCat.NRT_CONSTRUCTION or lcat == CST.FileReadCat.NRT_CONSTRUCTION:
            to_return.append(CST.Flags.NRT_FLAG_CONSTRUCTION)
        #             else:
        #                 to_return.append(CST.Flags.UNDEFINED)
        return to_return


    def bilan(self):
        """
        return a bilan for the test
        """
        to_print = " "+ CST.TestCategories.get_cst_pname(self.category).replace("NRT_CAT_", "")
        to_print += " -- " + self.directory + " " + self.recipe.name
        print(to_print)
        return

    @property
    def statu(self):
        return self.category == CST.TestCategories.NRT_CAT_OK

    def __repr__(self):
        to_print = ""
        to_print = " "+ CST.TestCategories.get_cst_pname(self.category).replace("NRT_CAT_", "")+" ("+str(self.statu)+")"
        to_print += " -- " + self.directory + " " + self.recipe.name+"\n"
        to_print += "\t- "+self.struct.recipe.replace(self.struct.directory, '.')+"\n"
        to_print += "\t- "+self.struct.state.replace(self.struct.directory, '.')+" "+CST.FileReadCat.get_cst_pname(self.ref_statu.valueCat)+"\n"
        to_print += "\t- "+self.struct.res.replace(self.struct.directory, '.')+" "+CST.FileReadCat.get_cst_pname(self.last_run_statu.valueCat)+"\n"
        return to_print
