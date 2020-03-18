#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/7
"""

import threading
import plugin.setting as setting
from model.ipmodel import Proxy
import queue
import traceback

from db.dbopera import CDbopera
from db.mongodbclient import CMongodbclient
from main.loghandle import LogHandler as mylogger

import time

# 多线程搜索代理网页，获取代理ip。
# 
""""""
# 动态加载库
import importlib


class CSpider(threading.Thread):
    
    def __init__(self, spidername, que, loghandle):
        threading.Thread.__init__(self)
        self.__spidername = spidername
        self.__spider = None
        self.__que = que
        self.log = loghandle
    
    def run(self):
        if hasattr(setting, "pluginlist"):
            if self.__spidername in setting.pluginlist:
                # __import__: 搜索model
                try:
                    self.__spider = getattr(__import__("plugin." + self.__spidername), self.__spidername)
                    #self.__spider = importlib.import_module("plugin." + self.__spidername)
                except Exception:
                    self.log.error(traceback.format_exc())
                    
        else:
            #self.log.LOG(action = "error", msg = "no plugin")
            self.log.error("no plugin")
            return
                    
        if self.__spider is not None:
            # self.log.LOG(action = "info", msg = self.__spidername + " is running")
            self.log.info(self.__spidername + " is running")
            try:
                proxylist = self.__spider.run()
                
                for proxy in proxylist:
                    prox = Proxy()
                    if isinstance(proxy, dict):
                        
                        try:
                            #print(proxy)
                            prox.ipaddress = proxy["ipaddress"]
                            prox.port =  proxy["port"]
                            prox.svradd =  proxy["svradd"]
                            prox.isanony =  proxy["isanony"]
                            prox.prototype =  proxy["prototype"]
                            prox.speed =  proxy["speed"]
                            prox.conntime =  proxy["conntime"]
                            prox.aliveminute =  proxy["aliveminute"]
                            prox.availidtime =  proxy["availidtime"]
                            self.__que.put(prox)
                            
                        except Exception:
                            self.log.error(traceback.format_exc() + "\n" + str(proxy))
                            continue
                
                # 爬过一次ip后，每天爬一次，每次只爬第一页
                setting.pagerange = 1
                self.log.info(self.__spidername + " end")
            except Exception:
                self.log.error(traceback.format_exc())
        else:
            self.log.error(self.__spidername + " isn't exists")

def Saveproxy(queue):
    
    mogclient = CMongodbclient()
    while not terminal:
        while not queue.empty():
        #while not queue.empty() and not terminal:
            
            proxy = queue.get()
            ret = mogclient.get({"proxyid": proxy.proxyid}, action = "one")
            if len(ret) == 1:
                if ret[0] is None:
                    mogclient.put(proxy)
                else:
                    # 当数据存在的情况，仅需要更新数据库上内容
                    ret[0]["frequency"] += 1
                    ret[0]["availidtime"] = proxy.availidtime
                    hashval = {"proxyid": proxy.proxyid}
                    newval = {"$set": {"frequency": ret[0]["frequency"], "availidtime": ret[0]["availidtime"]}}
                    
                    mogclient.modify(hashval, newval)
                    
        time.sleep(2)
                
def run():
    importlib.reload(setting)
    threadlog = mylogger()
    if hasattr(setting, "pluginlist"):
        if isinstance(setting.pluginlist, list):
            threadls = []
            que = queue.Queue()
            for spidplug in setting.pluginlist:
                thread = CSpider(spidplug, que, threadlog)
                threadlog.info(spidplug + " start")
                thread.start()
                threadls.append(thread)
                #print(spidplug)
                time.sleep(1)
            
            # 存储线程
            global terminal
            terminal = False
            svathre = threading.Thread(target = Saveproxy, args = (que,))
            svathre.setDaemon(True)
            svathre.start()
            
            flag = 0
            # 确保线程全部停掉，且共享队列中没有数据
            while flag != len(threadls) or not que.empty():
                #CDbopera.insert(que.get())
                if flag != len(threadls):
                    flag = 0
                    for thread in threadls:
                        if not thread.is_alive():
                            flag += 1
                
                time.sleep(8)
                
            terminal = True
            threadlog.info("all spiders end")
    return 
                
if __name__ == "__main__":
    run()