#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/8
"""

import pymongo
import traceback
from main.loghandle import LogHandler as mylogger
import json
#from main.loghandle import ERROR
import hashlib

threadlog = mylogger()

class CMongodbclient(object):
    
    def __init__(self, host = "127.0.0.1", port = 27017, dbname = "proxy", tabname = "proxys", **kwargs):
        #self.tablename = kwargs["name"]
        self.client = pymongo.MongoClient(host, port, **kwargs)
        # 默认获取代理数据库
        self.db = self.client[dbname]
        self.table = self.db[tabname]
    
    def changetable(self, tablename):
        self.tablename = tablename
        
        try:
            #if tablename in self.db.list_collection_names():
            self.table = self.db[tablename]
        except Exception:
            threadlog.error(traceback.print_exc())
    
    # 默认查询一条，action = "all"时批量查询
    def get(self, strwhere = {}, action = "one", limit = 100, skip = 0):
        ret = []
        try:
            if action == "one":
                ret.append(self.table.find_one(strwhere, {"_id":0}))            
            elif action == "all":
                ret.extend(list(self.table.find(strwhere, {"_id":0}).limit(limit).skip(skip)))
            else:
                ret = []
        except Exception:
            #TODO: 日志处理
            threadlog.error(traceback.print_exc())
            ret = []
                
        return ret
    
    
    def put(self, proxy):
        ret = ""
        try:
            if isinstance(proxy, dict):
                val = proxy
            else:
                val = proxy.items()
                
            ret = self.table.insert(val)
        except Exception:
            threadlog.error(traceback.print_exc())
            ret = ""
            
        return ret 
    
    def modify(self, hashval, newval):
        try:
            ret = self.table.update_one(hashval, newval)
        except Exception:
            raise ValueError(traceback.print_exc())
            
    def delete(self, hashval):
        try:
            querystr = {"hashval": hashval}
            self.table.delete(querystr)
        except Exception:
            threadlog.error(traceback.print_exc())
    
    def deleteall(self):
        self.table.remove({})
    
    def getTotal(self, strwhere = {}):
        return self.table.count(strwhere)
    
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 27017
    cc = CMongodbclient(ip, port)
#     dd = cc.get({"availidtime":""}, "all")
#     print(len(dd), dd[0])
    
    proxydi = {}
    
    pagesize = 100
    offset = 0
    count = cc.getTotal()
    
    # 获取页码 
    pagetotal = int(count / pagesize) + 1 if count % pagesize != 0 else 0
    
    retls = []
    
    for i in range(pagetotal):
        offset = pagesize * i
        for proxy in cc.get({}, action = "all", limit = pagesize, skip = offset):
            proxyval = str({"ip": proxy["ipaddress"], "port": proxy["port"], "prototype": proxy["prototype"].lower()})
            proxyid = hashlib.md5(proxyval.encode("utf-8")).hexdigest()
            #proxyid = proxy["proxyid"]
            
            proxydi[proxyid] = proxy.copy()
    
    #cc.deleteall()
    cc.changetable("proxyback")
    for key, value in proxydi.items():
        value["proxyid"] = key
        cc.put(value)
        
    
    #print(cc.modify({"proxyid": "578f95faac29770e09b2c3e74c1a5b8f"}, {"$set": {"frequency": 9}}))
    
    #for proxy in cc.get({"frequency": {"$gt": 0}}, action = "all"):
     #   print(proxy)
    
    
    