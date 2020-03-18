# coding:utf-8
'''
Created on 2020��3��1��

@author: cmck
'''

import logging
import os
from logging.handlers import TimedRotatingFileHandler


# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

import threading

class LogHandler(logging.Logger):
    def __init__(self, modulname = "", level = "DEBUG", isstream = True, isfile = True):
        self.modulname = modulname
        self.level = level
        #super(LogHandler, self).__init__(self, self.modulname, level)
        logging.Logger.__init__(self, self.modulname, level)
        
        if isstream:
            self.__setStreamHandler__(level)
        
        if isfile:
            self.__setFileHandler__(level)
    
    __lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            with cls.__lock:
                cls.instance = logging.Logger.__new__(cls)
        
        return cls.instance
        
    def __setFileHandler__(self, level = None):
        
        # 获取log路径
        logpath = os.path.dirname(os.path.abspath(__file__))
        logpath = os.path.dirname(logpath)
        logpath = logpath + "/logs/"
        
        if not os.path.exists(logpath):
            os.mkdir(logpath)

        # 获取本地时间，并转换为为相应格式的字符串
        # logname = logpath + time.strftime("%Y%m%d%H%M", time.localtime(time.time())) + ".log"
        logname = logpath + "maittt1.log"
        
        # fg = logging.FileHandler(logname, "r")
        fg = TimedRotatingFileHandler(filename = logname, when = "D", interval = 1, backupCount = 2, encoding = "utf-8")
        fg.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s-%(filename)s[line:%(lineno)d] - %(levelname)s : %(message)s")
        fg.setFormatter(formatter)

        self.filehandle = fg
        self.addHandler(fg)
        
    def __setStreamHandler__(self, level = None):
        
        formatter = logging.Formatter("%(asctime)s-%(filename)s[line:%(lineno)d] - %(levelname)s : %(message)s")
        #sh = logging.StreamHandler(sys.stdout)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)    
        self.addHandler(sh)
        
    def resetName(self, name):
        self.removeHandler(self.filehandle)
        self.__setFileHandler__()

if __name__ == "__main__":
    log = LogHandler("dddd")
    dd = LogHandler("sssd")
    log.info("text")
    print(dd is log)
        
        
        
        
        