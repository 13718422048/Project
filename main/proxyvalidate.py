#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/11/17
"""


import gevent

import os
import time


""""""
# from gevent import monkey
# monkey.patch_all()


import requests
import traceback
from db import dbopera as opera
from db import mongodbclient
import copy
import datetime
from main.loghandle import LogHandler as mylogger

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Checkproxy(object):
    def __init__(self):
        self.db = mongodbclient.CMongodbclient()
        self.threadlog = mylogger()
        self.threadlog.info("start checking proxy")
    
    
#     def __new__(cls):
#         if not hasattr(cls, "__instance"):
#             cls.__instance = super(Checkproxy,cls).__new__(cls)
#         return cls.__instance
    
    def getproxies(self, strwhere):
        """
        function：根据IP出现频率选择合适代理来做验证
        考虑效率问题，会分页读取数据，不过首先保证能够运转起来
        """
        
        pagesize = 100
        offset = 0
        count = self.db.getTotal(strwhere)
        
        # 获取页码 
        pagetotal = int(count / pagesize) + (1 if count % pagesize != 0 else 0)
        
        retls = []
        
        for i in range(pagetotal):
            offset = pagesize * i
            for proxy in self.db.get(strwhere, action = "all", limit = pagesize, skip = offset):
                
                retls.append(proxy)
                # 控制协程数目
                if len(retls) >= pagesize:
                    yield copy.deepcopy(retls)
                    retls = []
            
            # 清空内存
            if len(retls) != 0:
                yield copy.deepcopy(retls)
                retls = []
                
    def validateips(self, proxy):
        ip = proxy["ipaddress"]
        protocol = proxy["prototype"].lower()
        port = proxy["port"]
        urls = {"http": "http://httpbin.org/ip", "https" : "https://www.baidu.com"}
        httpproxy = {}
        flag = -1
        
        if protocol.find(",") > -1:
            for proto in protocol.split(","):
                url = urls[proto]
                httpproxy[proto] = "{0}://{1}:{2}".format(proto, ip, port)
                
        else:
            url = urls[protocol]
            httpproxy = {protocol : "{0}://{1}:{2}".format(protocol, ip, port)}
            
        session = requests.Session()
        try:
            req = session.get(url, proxies = httpproxy, timeout = (3,6), verify = False)
            if req.status_code == 200:
                flag = 1
            
        except Exception:
            flag = -1
        
        return flag
    
    def updateproxies(self, proxy, status):
        
        try:
            # 避免协程无返回结果时出现的错误
            if status is None:
                status = -1
                
            proxy["frequency"] = proxy["frequency"] + status
            
            # 设置上下限
            if proxy["frequency"] <= 0:
                proxy["frequency"] = 0
                
            if proxy["frequency"] >= 30:
                proxy["frequency"] = 30
                
            proxyid = proxy["proxyid"]
            proxy["availidtime"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
            
            return self.db.modify({"proxyid": proxyid}, {"$set": {"frequency": proxy["frequency"], "availidtime": proxy["availidtime"]}})
        except Exception:
            self.threadlog.error(traceback.format_exc() + "\n" + str(proxy) + + "\n" + str(status))
            return -1
        
    def checkproxies(self, strwhere = {"frequency": {"$gt" : 0}}):
        
        #strwhere = {"frequency": 0}
        total = self.db.getTotal(strwhere)
        for proxys in self.getproxies(strwhere):
            glist = []
            for proxy in proxys:
                g = gevent.spawn(self.validateips, proxy)
                glist.append(g)
            
            gevent.joinall(glist, timeout = 10)
            
            for i, proxy in enumerate(proxys):
                self.updateproxies(proxy, glist[i].value)
                
                if glist[i].value == 1:
                    yield total, proxy
            
            # 强制结束“挂起”的协程
            try:
                gevent.killall(glist)
            except Exception:
                self.threadlog.error("coordinations stop failure!")
                pass
        
        return 
    
    def getvalidproxy(self):
        
        proxy = dict()
        iter = 0
        flag = 0
        # 获取到可用代理，且寻找次数小于100
        while flag != 1 and iter < 100:
            iter += 1
            for para in self.getproxies():
                flag = self.validateips(para)
                if flag == 1:
                    proxy = para.copy()
                    yield proxy
                    #break
        #return proxy


# 验证可用 proxy的状态
def refresh(interval):
    cc = Checkproxy()
    ddlog = mylogger()
    strwhere = {"frequency": {"$gt" : 0}}
    
    while True:
        ddlog.info("refresh is running")
    
        total = 0
        sum = 0
        for total, proxy in cc.checkproxies(strwhere):
            sum += 1
        
        ddlog.info("total proxy is {0}, {1} is validating".format(total, sum))
        print("refresh sleep {0}s".format(interval))
        time.sleep(interval)
    

# 从无用的代理中筛选出可用代理
def filter(interval):
    cc = Checkproxy()
    ddlog = mylogger()
    strwhere = {"frequency": 0}
    
    while True:
        ddlog.info("filter is running")
        
        total = 0
        sum = 0
        for total, proxy in cc.checkproxies(strwhere):
            sum += 1
            
        ddlog.info("total proxy is {0}, {1} is validating".format(total, sum))
        print("filter sleep {0}s".format(interval))
        time.sleep(interval)
    
    
# 验证步骤
# 1. 获取待验证的权重大于零的代理proxy；
# 2. 限定超时时间，逐次验证各代理proxy（单进程，多线程，多协程）;
# 3. 将有效的proxy增加权重并存放至数据库中；无效的proxy减少权重并存放数据库中

if __name__ == "__main__":
    
    cc = Checkproxy()
    
    #for proxy in cc.getproxies():
    #    print(proxy)
    
    
    #for proxy in cc.getvalidproxy():
     #   print(proxy)
     
    strwhere = {"frequency": {"$gt" : 0}}
    #strwhere = {"frequency": 0}
    
    import time
    while True:
        for proxy in cc.checkproxies(strwhere):
            print(proxy)
            
        time.sleep(60)
    
    # 
    
    