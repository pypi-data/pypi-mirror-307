#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-09-28 09:24:04.952942"
__version__ = 1.0
# **************************************************
import os
import inspect
from . import constantes as CST


class VerbosityManager():
    def __init__(self, verbosity_level:int=3):
        self._verbosity = verbosity_level
        return

    @property
    def verbosity(self):
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value:int):
        self._verbosity = value


class NRT_ENV_VARIABLES:
    NRT_RECIPE_EXT = ".recipe"          # extenstion of the recipe file
    NRT_RESULT_EXT = ".res"             # extension of the last run ouput (produced by the recipe file)
    NRT_STATE_EXT = ".state"            # extension of the reference output
    NRT_DIR_RESULTS = ".test_results"   # directory where to find foo.res and foo.state files asssociated relative to foo.recipe
    NRT_COLOR_MODE = 1                  # active (1) / desactive (0) the color mode
    NRT_VERBOSITY_LEVEL = 0             # level of verbosity {0,1,2,3}
    # DOC END NRT_ENV_VARIABLES             do not remove this comment that is usefful for the doc


class Config():
    VAR_PATTERN = "NRT_"

    def __init__(self):
        self._set_config()
        return

    def _set_config(self):
        env_vars = {k: val for k, val in list(NRT_ENV_VARIABLES().__class__.__dict__.items()) if k.startswith(self.VAR_PATTERN)}
        for var in env_vars.keys():
            env_var = os.getenv(var)
            if env_var:
                if type(env_vars[var]).__name__ == 'int':
                    try:
                        env_var = int(env_var)
                    except:   # pragma: no cover
                        raise RuntimeError("Can't convert {} to int to set {}".format(env_var, var))
                self.__setattr__(var, env_var)
            else:
                self.__setattr__(var, env_vars[var])
        return


    def __setattr__(self, name, value):
        match(name):
            case 'NRT_COLOR_MODE':
                if value not in [0, 1]:
                    print('WARNING: NRT_COLOR_MODE is out of bound (bounds ares [0,1] and requeted is {})'.format(value))
                    new_value = 0 if value == 0 else 1
                    value = new_value
                    print('\t-> reset it to {}'.format(value))
            case 'NRT_VERBOSITY_LEVEL':
                if value > 4 or value < 0:
                    print('WARNING: NRT_VERBOSITY_LEVEL is out of bound (bounds ares [0-4] and requeted is {})'.format(value))
                    new_value = min(4, value)
                    new_value = max(0, new_value)
                    value = new_value
                    print('\t-> reset it to {}'.format(value))

            case _:
                pass
        return object.__setattr__(self, name, value)

    def __repr__(self):
        to_ret = ""
        for k, val in self.__dict__.items():
            if k.startswith(self.VAR_PATTERN):
                to_ret += "{} -> {}\n".format(k, val)
        return to_ret


conf = Config()


def get_color_fmt():
    if conf.NRT_COLOR_MODE == 1:
        return CST.ColorActivated
    else:
        return CST.ColorRemove
