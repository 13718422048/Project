# coding:utf-8
'''
Created on 2020��2��27��

@author: cmck
'''

import logging
import os
import time
import traceback
from logging.handlers import TimedRotatingFileHandler
import threading
import sys

class Logger(object):
    
    __lock = threading.Lock()
    
    def __init__(self):
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        
        logpath = os.path.dirname(os.path.abspath(__file__))
        logpath = os.path.dirname(logpath)
        logpath = logpath + "/logs/"
        
        if not os.path.exists(logpath):
            os.mkdir(logpath)

        # 获取本地时间，并转换为为相应格式的字符串
        # logname = logpath + time.strftime("%Y%m%d%H%M", time.localtime(time.time())) + ".log"
        logname = logpath + "main.log"
        # fg = logging.FileHandler(logname, "r")
        fg = TimedRotatingFileHandler(filename = logname, when = "D", interval = 1, backupCount = 2, encoding = "utf-8")
        fg.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s-%(filename)s[line:%(lineno)d] - %(levelname)s : %(message)s")
        fg.setFormatter(formatter)
        
        #sh = logging.StreamHandler(sys.stdout)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        
        self.logger.addHandler(fg)
        self.logger.addHandler(sh)
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            with cls.__lock:
                cls.instance = super(Logger, cls).__new__(cls, *args, **kwargs)
                
        return cls.instance
    
    def LOG(self, action = "info", msg = "", **kwargs):
        with self.__lock:
            if action == "critical":
                self.logger.critical(msg, **kwargs)
            elif action == "info":
                self.logger.info(msg, **kwargs)
            elif action == "warning":
                self.logger.warning(msg, **kwargs)
            elif action == "error":
                self.logger.error(msg, **kwargs)
            else:
                # 默认是debug
                self.logger.debug(msg, **kwargs) 
    
if __name__ == "__main__":
    pass

