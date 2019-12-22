#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/11/17
"""

import os
import requests
import traceback
import time
from db import dbopera as opera

import gevent
from gevent import monkey
monkey.patch_all()

class Checkproxy(object):
    def __init__(self):
        pass
    
    
    def getproxies(self, weight = 0):
        """
        function：根据IP出现频率选择合适代理来做验证
        考虑效率问题，会分页读取数据，不过首先保证能够运转起来
        """
        strwhere = "frequency > " + str(weight)
        for proxy in opera.query(strwhere):
            yield proxy
        
    def validateips(self, proxy):
        ip = proxy.ipaddress
        protocol = proxy.prototype
        port = proxy.port
        url = "http://httpbin.org/ip"
        
        httpproxy = {protocol : "{0}://{1}:{2}".format(protocol, ip, port)}
        session = requests.Session()
        try:
            req = session.get(url, proxyies = httpproxy, timeout = 10, verify = False)
            if req == 200:
                return 1
            
        except Exception as e:
            traceback.print_exc()
            
        return -1
    
    def updateproxies(self, proxy, status):
        
        proxy.frequency = proxy.frequency + status 
        try:
            return opera.modify(proxy)
        except Exception as e:
            return -1
        
        
    def checkproxies(self):
        for proxy in self.getproxies():
            ret = self.updateproxies(proxy, self.validateips(proxy))
            yield ret, proxy


# 验证步骤
# 1. 获取待验证的权重大于零的代理proxy；
# 2. 限定超时时间，逐次验证各代理proxy（单进程，多线程，多协程）;
# 3. 将有效的proxy增加权重并存放至数据库中；无效的proxy减少权重并存放数据库中


if __name__ == "__main__":
    print("ffff")
    
    
    
    
    
    