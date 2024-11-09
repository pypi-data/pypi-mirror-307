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


def test_flags():
    PATH = os.path.join(os.path.dirname(__file__), "01-TEST-BASE-EXAMPLES")

    RES = {'./01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/00-TEST-ALWAYS-OK/runme.recipe': [0],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/00-TEST-ALWAYS-OK/runme1.recipe': [0],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/01-TEST-WITHOUT-RES/runme.recipe': [-1, -5],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/02-TEST-WITHOUT-REF/runme.recipe': [-2, -6],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/03-TEST_NO_READABLE_REF/runme.recipe': [-3, -6],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/04-TEST_NO_READABLE_RES/runme.recipe': [-4, -5],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/05-TEST-DOWNGRADED-RES-BROKEN/runme.recipe': [-5],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/06-TEST-FIXED-REF-BROKEN/runme.recipe': [-6],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/07-TEST-OK-BUT-NOT-NOMINAL/runme.recipe': [-7],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/08-TEST-UNDEFINED/runme.recipe': [-8],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/09-TEST-UNDER-CONSTRUCTION/runme.recipe': [-2, 999],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/10-TEST-WITHOUT-REF-AND-RES/runme.recipe': [-2, -1],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/11-TEST-NO_READABLE_REF-AND-RES/runme.recipe': [-3, -4],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/12-TEST-REF-FAILED/runme.recipe': [-7],
           './01-TEST-BASE-EXAMPLES/02-CHECK-RUN/01-RUN-OK/runme.recipe': [0],
           './01-TEST-BASE-EXAMPLES/02-CHECK-RUN/02-RUN-KO/runme.recipe': [-5],
           './01-TEST-BASE-EXAMPLES/02-CHECK-RUN/03-RUN-FAILED/runme.recipe': [-1,-5],
           './01-TEST-BASE-EXAMPLES/02-CHECK-RUN/04-RUN-UNDER-CONSTRUCTION/runme.recipe': [-2, 999]
           }

    # --------------------------------------------------
    # verbosity_level=0
    # --------------------------------------------------
    for verbosity in range(5):
        test_cases = None
        test_cases = GTB.test_cases(path=PATH,
                                    ext=NRT_RECIPE_EXT,
                                    verbosity_level=verbosity)

        test_cases.run()
        test_cases.print_bilan()
        flags = test_cases.flags()
        assert(len(list(flags.keys())) == len(list(RES.keys())))
        for k, val in flags.items():
            k_rel = k.replace(os.path.dirname(__file__),'.')
            assert(RES[k_rel] == val)
    # --------------------------------------------------


    # --------------------------------------------------
    # test regex filter
    # --------------------------------------------------
    RES = {'./01-TEST-BASE-EXAMPLES/02-CHECK-RUN/01-RUN-OK/runme.recipe': [0],
           './01-TEST-BASE-EXAMPLES/02-CHECK-RUN/02-RUN-KO/runme.recipe': [-5],
           './01-TEST-BASE-EXAMPLES/02-CHECK-RUN/03-RUN-FAILED/runme.recipe': [-1, -5],
           './01-TEST-BASE-EXAMPLES/02-CHECK-RUN/04-RUN-UNDER-CONSTRUCTION/runme.recipe': [-2, 999]}
    test_cases = GTB.test_cases(path=PATH,
                                regex="02-CHECK-RUN",
                                ext=NRT_RECIPE_EXT,
                                verbosity_level=4)
    test_cases.run()
    print(test_cases)
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        k_rel = k.replace(os.path.dirname(__file__), '.')
        assert(RES[k_rel] == val)
    # --------------------------------------------------


    # --------------------------------------------------
    # recusrive option
    # --------------------------------------------------
    test_cases = GTB.test_cases(path=PATH,
                                recursive = False,
                                ext=NRT_RECIPE_EXT,
                                verbosity_level=4)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert({} == flags)
    # --------------------------------------------------

    # --------------------------------------------------
    # test filter_name
    # --------------------------------------------------
    RES = {
        './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/04-TEST_NO_READABLE_RES/runme.recipe': [-4, -5],
        './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/11-TEST-NO_READABLE_REF-AND-RES/runme.recipe': [-3, -4],
    }
    test_cases = GTB.test_cases(path=PATH,
                                filter_name="NRT_FLAG_NO_READABLE_RES",
                                ext=NRT_RECIPE_EXT,
                                verbosity_level=4)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        k_rel = k.replace(os.path.dirname(__file__), '.')
        assert(RES[k_rel] == val)
    # --------------------------------------------------

    # --------------------------------------------------
    # test filter_name
    # --------------------------------------------------
    RES = {
        './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/04-TEST_NO_READABLE_RES/runme.recipe': [-4, -5],
        './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/11-TEST-NO_READABLE_REF-AND-RES/runme.recipe': [-3, -4],
    }
    test_cases = GTB.test_cases(path=PATH,
                                filter_name="NRT_FLAG_NO_READABLE_RES",
                                ext=NRT_RECIPE_EXT,
                                verbosity_level=4)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        k_rel = k.replace(os.path.dirname(__file__), '.')
        assert(RES[k_rel] == val)
    # --------------------------------------------------


    # --------------------------------------------------
    # verbosity_level=0
    # --------------------------------------------------
    RES = {'./01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/00-TEST-ALWAYS-OK/runme.recipe': [0],
           './01-TEST-BASE-EXAMPLES/01-CHECK-STATUS/00-TEST-ALWAYS-OK/runme1.recipe': [0],
           './01-TEST-BASE-EXAMPLES/02-CHECK-RUN/01-RUN-OK/runme.recipe': [0],
           }
    test_cases = GTB.test_cases(path=PATH,
                                filter_name="NRT_FLAG_OK",
                                ext=NRT_RECIPE_EXT,
                                verbosity_level=0)
    test_cases.run()
    test_cases.print_bilan()
    flags = test_cases.flags()
    assert(len(list(flags.keys())) == len(list(RES.keys())))
    for k, val in flags.items():
        k_rel = k.replace(os.path.dirname(__file__), '.')
        assert(RES[k_rel] == val)

    # --------------------------------------------------
