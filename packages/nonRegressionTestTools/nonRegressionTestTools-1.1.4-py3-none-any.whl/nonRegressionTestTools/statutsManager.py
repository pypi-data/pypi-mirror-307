#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************
__author__  = "Teddy Chantrait"
__email__   = "teddy.chantrait@gmail.com"
__status__  = "Development"
__date__    = "2024-04-26 14:16:13.359025"
__version__ = 1.0
# **************************************************
from . import constantes as CST
from . import config as CONF
from . import testCase as TC
import os

class FileInfo():

    def __init__(self, fn:str="", cwd:str=None):
        self._fn = fn
        self._cwd = cwd
        self._fullFilePath = None  # propertie fill by initial_process
        self._relFilePath = None  # propertie fill by initial_process
        self._name = None  # propertie fill by initial_process
        self._baseName = None  # propertie fill by initial_process
        self._ext = None   # propertie fill by initial_process
        self._abs_dir = None   # propertie fill by initial_process
        self._rel_dir = None   # propertie fill by initial_process
        self._valid = None
        self._initial_process()

    def _initial_process(self):
        self._valid = CST.Boolean.NRT_OK
        self._name = os.path.basename(self._fn)
        splitFile = os.path.splitext(self._name)
        self._baseName = splitFile[0]
        self._ext = splitFile[1]

        self._fullFilePath = self._fn
        if not(os.path.isfile(self._fn)):   #pragma: no cover
            try:
                self._fullFilePath = os.path.join(os.getcwd(), self._fn)
                if not(os.path.isfile(self._fullFilePath)):
                    self._valid = CST.Boolean.NRT_KO
                    return
            except:
                self._valid = CST.Boolean.NRT_KO
                return
        self._abs_dir = os.path.dirname(self._fullFilePath)

        if self._cwd is not None:
            if not os.path.isdir(self._cwd):   #pragma: no cover
                self._valid = CST.Boolean.NRT_KO
            else:
                try:
                    self._rel_dir = "./"+self._abs_dir.split(self._cwd)[-1][1:]
                    abs_p = os.path.join(str(self._cwd), str(self._rel_dir))
                    self._fullFilePath = os.path.join(abs_p,self._fn)

                    if not os.path.isdir(abs_p):   #pragma: no cover
                        print("Warning relative path can be constructed\n current work dir \n {}\n path".foramt(self._cwd, self._abs_dir))
                        raise RuntimeError
                except:   #pragma: no cover
                    self._rel_dir = None


    @property
    def fn(self):
        return self._fullFilePath

    @property
    def valid(self):
        return self._valid

    @property
    def name(self):
        return self._name

    @property
    def baseName(self):
        return self._baseName

    @property
    def ext(self):
        return self._ext

    @property
    def fDirPath(self):
        return self._abs_dir
    @property
    def rDirPath(self):
        return self._rel_dir

    @property
    def cwd(self):
        return self._cwd

    def  __repr__(self):
        to_ret = ""
        to_ret += "File info:\n"
        to_ret += "\t file: {}\n".format(self.fn)
        to_ret += "\t name: {}\n".format(self.name)
        to_ret += "\t baseName: {}\n".format(self.baseName)
        to_ret += "\t ext: {}\n".format(self.ext)

        to_ret += "\t valid: {}\n".format(CST.Boolean.get_cst_pname( self.valid))
        to_ret += "\t cwd: {}\n".format( self.cwd)
        to_ret += "\t dir full: {}\n".format(self.fDirPath)
        to_ret += "\t dir rela: {}\n".format(self.rDirPath)
        return to_ret


class FileStatu():

    @classmethod
    def get(cls, filePath):
        ifile = FileInfo(fn=filePath)
        # print(fileTest)
        fileStatu = FileStatu(fn=filePath)
        fileStatu.openStat = ifile.valid
        if ifile.valid:
            with open(filePath, 'r') as f1:
                try:
                    line = f1.readline().rstrip()
                    fileStatu.value = line
                    fileStatu.readStatu = CST.Boolean.NRT_OK
                except: # pragma: no cover
                    fileStatu.readStatu = CST.Boolean.NRT_KO
        return fileStatu


    def __init__(self, fn):
        self._fn = fn
        self._openStat = CST.Boolean.NRT_KO
        self._readStat = CST.Boolean.NRT_KO
        self._valueValid = CST.Boolean.NRT_KO
        self._valueCat = CST.FileReadCat.NRT_OTHERS
        self._value = None

    @property
    def fn(self):
        return self._fn


    @property
    def openStat(self):
        return self._openStat

    @openStat.setter
    def openStat(self, val):
        dic = CST.Boolean.get_cst_dict()
        if val in list(dic.values()):
            self._openStat = val
        else:
            self._openStat = None  # pragma: no cover

    @property
    def readStatu(self):
        return self._readStat

    @readStatu.setter
    def readStatu(self, val):
        dic = CST.Boolean.get_cst_dict()
        if val in list(dic.values()):
            self._readStat = val
        else:
            self._readStat = None   # pragma: no cover

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

        try:
            val = int(val)

            dic = CST.FileWriteCat.get_cst_dict()
            if val in list(dic.values()):
                self._valueCat = val
            else:
                self._valueCat = CST.FileReadCat.NRT_OTHERS
            self._valueValid = CST.Boolean.NRT_OK
        except:
            self._valueValid = CST.Boolean.NRT_KO
            self._valueCat = CST.FileReadCat.NRT_OTHERS

    @property
    def valueValid(self):
        return self._valueValid


    @valueValid.setter
    def valueValid(self, val):
        print("try to set vla", val)
        if val in list(CST.Boolean.get_cst_dict().values()):
            self._valueValid = val
        else:
            self._valueValid = CST.Boolean.NRT_KO
        return

    @property
    def valueCat(self):
        return self._valueCat

    @valueCat.setter
    def valueCat(self, val):
        print("try to set vla", val)
        if val in list(CST.FileReadCat.get_cst_dict().values()):
            self._valueCat = val
        else:
            self._valueCat = CST.FileReadCat.NRT_OTHERS
        return

    def  __eq__ (self, obj):
        if not isinstance(obj, self.__class__):
            return False
        else:
            return self.openStat == obj.openStat and self.readStatu == obj.readStatu and self.value == obj.value and self.valueCat == obj.valueCat and self.valueValid == obj.valueValid

    def  __repr__(self):
        to_ret = ""
        to_ret += "File statu:\n"
        to_ret += "\tfile: {} \n".format(self.fn)
        to_ret += "\topen statu: {} ({})\n".format(CST.Boolean.get_cst_pname(self.openStat), self.openStat)
        to_ret += "\tread statu: {} ({})\n".format(CST.Boolean.get_cst_pname(self.readStatu), self.readStatu)
        to_ret += "\tvalid: {} ({})\n".format(CST.Boolean.get_cst_pname(self.valueValid), self.valueValid)
        to_ret += "\tcat: {} ({})\n".format(CST.FileReadCat.get_cst_pname(self.valueCat), self.valueCat)
        to_ret += "\tvalue: {}\n".format(self.value)
        return to_ret
