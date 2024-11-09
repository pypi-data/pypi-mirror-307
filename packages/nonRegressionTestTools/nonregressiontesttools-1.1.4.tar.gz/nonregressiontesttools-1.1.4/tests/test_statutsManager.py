from nonRegressionTestTools import statutsManager as STM
from nonRegressionTestTools import constantes as CST
from nonRegressionTestTools import config as CONF
import os
import pytest
VERBOSITY = 1

def test_FileInfo():
    fn = "file.recipe"
    fn = os.path.join(os.path.dirname(__file__), "00-DATA", fn)
    fileInfo = STM.FileInfo(fn=fn)
    if VERBOSITY:
        print(fileInfo)

    fn = "file.recipe"
    cwd = os.getcwd()
    fn = os.path.join(cwd, "00-DATA", fn)

    fileInfo = STM.FileInfo(fn=fn, cwd=os.path.join(os.path.dirname(__file__), "00-DATA"))
    if VERBOSITY:
        print(fileInfo)


    fileInfo = STM.FileInfo(fn='fake.dat', cwd=os.path.join(os.path.dirname(__file__), "00-DATA"))
    if VERBOSITY:
        print(fileInfo)

def test_FileStatu():
    DATA_DIR = "00-DATA"
    outvals = CST.FileWriteCat.get_cst_dict()
    if VERBOSITY:
        print("CAT:\n",CST.FileWriteCat())
    for k, val in outvals.items():
        fn = "file_{}{}".format(k, CONF.NRT_ENV_VARIABLES.NRT_RESULT_EXT)
        fres = os.path.join(os.path.dirname(__file__),DATA_DIR, fn)
        with open(fres, "w") as f1:
            f1.writelines(str(val))
        fres_statu = STM.FileStatu.get(fres)

        fstate = fres.replace(CONF.NRT_ENV_VARIABLES.NRT_RESULT_EXT,
                              CONF.NRT_ENV_VARIABLES.NRT_STATE_EXT)
        fstat_statu = STM.FileStatu.get(fstate)
        if VERBOSITY:
            print(fres_statu)
        assert(fres_statu == fstat_statu)

    # --------------------------------------------------
    fn = "file_wong_output"+CONF.NRT_ENV_VARIABLES.NRT_RESULT_EXT
    fres = os.path.join(os.path.dirname(__file__),DATA_DIR, fn)
    with open(fres, "w") as f1:
        f1.write("100\n")

    fres_statu = STM.FileStatu.get(fres)

    fstate = fres.replace(CONF.NRT_ENV_VARIABLES.NRT_RESULT_EXT,
                          CONF.NRT_ENV_VARIABLES.NRT_STATE_EXT)

    fstat_satu = STM.FileStatu.get(fstate)

    if VERBOSITY:
        print(fres_statu)
    assert(fres_statu == fstat_satu)
    # --------------------------------------------------

    # --------------------------------------------------
    fn = "file_not_readable"+CONF.NRT_ENV_VARIABLES.NRT_RESULT_EXT
    fres = os.path.join(os.path.dirname(__file__),DATA_DIR, fn)
    with open(fres, "w") as f1:
        f1.write("NOT READABLE\n")

    fres_statu = STM.FileStatu.get(fres)

    fstate = fres.replace(CONF.NRT_ENV_VARIABLES.NRT_RESULT_EXT,
                          CONF.NRT_ENV_VARIABLES.NRT_STATE_EXT)

    fstat_satu = STM.FileStatu.get(fstate)

    if VERBOSITY:
        print(fres_statu)
    assert(fres_statu == fstat_satu)
    # --------------------------------------------------

    # --------------------------------------------------
    fn = "file_missing.state"
    fn_res = os.path.join(DATA_DIR, fn)

    fstat = STM.FileStatu.get(fn_res)
    if VERBOSITY:
        print(fstat)
    fstat_REF = STM.FileStatu(fn_res)
    fstat_REF.openStat = CST.Boolean.NRT_KO
    fstat_REF.readStatu = CST.Boolean.NRT_KO

    fstat_REF.valueCat = "CANT SET THIS"
    fstat_REF.valueCat = CST.FileReadCat.NRT_OTHERS
    fstat_REF.valueValid = "CANT SET THIS"
    fstat_REF.valueValid = CST.Boolean.NRT_KO
    fstat_REF.value = None
    assert(fstat == fstat_REF)
    assert((fstat== "Cant compare to this") == False)

    # --------------------------------------------------
