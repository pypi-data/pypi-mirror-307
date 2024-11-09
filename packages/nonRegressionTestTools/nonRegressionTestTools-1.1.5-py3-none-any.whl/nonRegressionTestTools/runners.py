#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-04-26 14:11:18.859839"
__version__ = 1.0
# **************************************************
from . import constantes as CST
from . import config as CONF
import subprocess


class IntRunner(CONF.VerbosityManager, object):
    """
    interface class to define a runner
    """
    def __init__(self,  cmd_file:str, abs_dir:str, **kwd):
        super().__init__(**kwd)
        self._cmd_file = cmd_file
        self._abs_dir = abs_dir
        self._runner_type = None
        self._iProc = None
        self._iProcId = None
        self._job_receipies = None
        self._signal = None
        self._set_job_receipies()
        self.stdout = ""
        self.stderr = ""
        self._is_job_terminate = False
        self._is_job_submitted = False
        return

    def _set_job_receipies(self):
        assert not hasattr(super(), '_set_job_receipies')   # pragma: no cover
        raise NotImplementedError("Must override ")         # pragma: no cover

    def _submit_job(self):
        assert not hasattr(super(), '_submit_job')          # pragma: no cover
        raise NotImplementedError("Must override ")         # pragma: no cover

    def _get_job_id(self):
        assert not hasattr(super(), '_get_job_id')          # pragma: no cover
        raise NotImplementedError("Must override ")         # pragma: no cover

    def _wait_job_complet(self):
        assert not hasattr(super(), '_wait_job_complet')    # pragma: no cover
        raise NotImplementedError("Must override ")         # pragma: no cover

    def _print_sorties_after_job_terminate(self):
        print("Warning print sorties methode not defined")  # pragma: no cover
        return                                              # pragma: no cover

    def run(self):
        """
        run the given commande file
        """
        if self._verbosity > 0:
            print("CMD: {}".format(self._job_receipies))
        self._submit_job()
        self._is_job_submitted = True
        self._get_job_id()
        if self._verbosity > 0:
            print("job subbmited (PID: {})".format(self._iProcId))
        self._wait_job_complet()
        self._is_job_terminate = True
        if self._verbosity > 0:
            print("job terminate (PID: {})".format(self._iProcId))
        if self._verbosity > 0:
            print("EXEC SIGNAL: {}".format(self._signal))
            if self._verbosity >= 2:
                self._print_sorties_after_job_terminate()
        return

    def info(self): # pragma: no cover
        to_print = "CMD: {}".format(self._job_receipies)
        if self._is_job_submitted:
            to_print += "\nPID: {}".format(self._iProcId)
        else:
            to_print += "\nJob not submitted"
        if self._is_job_terminate:
            to_print += "\nEXEC SIGNAL: {}".format(self._signal)
        else:
            if self._is_job_submitted:
                to_print += "\nJob not terminate"
        return to_print

    def __repr__(self):  # pragma: no cover
        to_print = self.info()
        to_print += "\n"
        to_print += str(self.stdout)
        to_print += str(self.stderr)
        return to_print
# --------------------------------------------------


class BashRunner(IntRunner):
    """
    Sepcify a bash runner
    """
    def __init__(self, **kwd):
        super().__init__(**kwd)
        return

    def _set_job_receipies(self):
        self._job_receipies = 'cd {} && . {}'.format(self._abs_dir,
                                                self._cmd_file)
        return

    def _submit_job(self):
        self._iProc = subprocess.Popen(self._job_receipies,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       executable='/usr/bin/bash',
                                       shell=True)
        return

    def _get_job_id(self):
        if self._iProc:
            self._iProcId = self._iProc.pid
        return

    def _wait_job_complet(self):
        if self._iProc:
            self._iProc.wait()
            self.stdout = [iline.decode() for iline in self._iProc.stdout.readlines()]
            # for iline in :
            #     self._stdout += iline.decode().rstrip()
            # for iline in self._iProc.stderr.readlines():
            #     self._stderr += iline.decode().rstrip()
            self.stderr = [iline.decode() for iline in self._iProc.stderr.readlines()]
            self._signal = self._iProc.poll()
        return

    def _print_sorties_after_job_terminate(self):
        print("+"*50)
        print("stdout:")
        print("+"*50)
        for iline in self.stdout:
            print("  | ", iline.rstrip())
        print("+"*50)
        print()
        print("+"*50)
        print("stderr:")
        print("+"*50)
        for iline in self.stderr:
            print("  | ", iline.rstrip())
        print("+"*50)
        return
# --------------------------------------------------
