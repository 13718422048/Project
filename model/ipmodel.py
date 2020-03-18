#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/7
"""

import re
import hashlib
import json
import copy

class Proxy:
    
    def __init__(self):
        self.__items = dict()
        # ip
        self.__ipaddress = ""
        # 端口
        self.__port = 0
        # ip所在地址
        self.__svradd = ""
        # 匿名状态
        self.__isanony = "匿名"
        # 协议类型: HTTP /　HTTPS
        self.__prototype = ""
        # 连接速度
        self.__speed = ""
        # 连接时长
        self.__conntime = ""
        # 存活时长
        self.__aliveminute = 0
        # 验证时间
        self.__availidtime = ""
        # ip被使用频次，默认为1次，上限为30次。为零的ip不会再被取出，会隔一段时间重新验证。
        self.__frequency = 1
        # 随机生成一个哈希值，用于标识代理
        self.__proxyid = ""
    
    
    def items(self):
        # 需要根据ip、端口、地址及协议的四元组来构成
        
        classname = self.__class__.__name__
    
        proxy = dict()
        for key, value in vars(self).items():
            if key.find("__items") != -1:
                continue
            
            proxy[key.replace("_" + classname +"__", "")] = value
        
        self.__items = proxy.copy()
        return proxy
    
    def __str__(self):
        return json.dumps(self.__items, ensure_ascii = False)
    
    @property
    def speed(self):
        return self.__speed
    @speed.setter
    def speed(self, vale):
        value = str(vale).replace(" ", "")
        self.__speed = value.replace("秒", "")
    
    @property
    def proxyid(self):
        proxyval = str({"ip": self.__ipaddress, "port": self.__port, "prototype": self.__prototype.lower()})
        self.__proxyid = hashlib.md5(proxyval.encode("utf-8")).hexdigest()
        return self.__proxyid 
    
    @property
    def ipaddress(self):
        return self.__ipaddress
    @ipaddress.setter
    def ipaddress(self, ip):
    # ip格式校验
        isip = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", ip)
        if isip is not None and len(isip) != 0:
            self.__ipaddress = isip[0]
        else:
            raise ValueError("错误ip")

    @property
    def port(self):
        return self.__port
    @port.setter
    def port(self, port):
        if(isinstance(port, str) and port.isdigit()):
            if(int(port) > 0 and int(port) < 65535):
                self.__port = port
            else:
                raise ValueError("该值不在0~65535之间")
        else:
            raise ValueError("该值不是数字")
                
    @property
    def svradd(self):
        return self.__svradd    
    @svradd.setter
    def svradd(self, serveradd):
        self.__svradd = serveradd
    
    @property
    def prototype(self):
        return self.__prototype
    @prototype.setter
    def prototype(self, value):
        value = str(value).replace(" ", "")
        if value.lower() not in ["http", "https"]:
            self.__prototype = "http"
            
        else:
            self.__prototype = value
            
    @property
    def isanony(self):
        return self.__isanony
    @isanony.setter
    def isanony(self, value):
        value = str(value).replace(" ", "")
        """annonytype = {
            "透明" : 0,
            "高匿" : 1,
            "普匿" : 2,
            "未知" : 3,
            "高匿名" : 1,
            "" : 4
                }"""
        #self.__isanony = annonytype.get(value, None)
        self.__isanony = value
        
    @property
    def aliveminute(self):
        return self.__aliveminute
    @aliveminute.setter
    def aliveminute(self, aliveminuteval):
        try:
            value = str(aliveminuteval).replace(" ", "")
            days = 0
            hours = 0
            minutes = 0
            
            if value.find("天") > -1:
                days = int(value.split("天")[0]) * 24 * 60
                value = value.split("天")[1]
                
            if value.find("小时") > -1:
                hours = int(value.split("小时")[0]) * 60
                value = value.split("小时")[1]
            
            if value.find("分") > -1 or value.find("分钟") > -1:
                value = value.replace("分钟", "分")
                minutes = int(value.split("分")[0])
                
            self.__aliveminute = days + hours + minutes
            
        except ValueError as vale:
            raise ValueError(vale + value)
            
    @property
    def frequency(self):
        return self.__frequency
    @frequency.setter
    def frequency(self, value):
        self.__frequency = value
        
        
if __name__ == "__main__":
    proxyval = "222"
    dd = hashlib.md5(proxyval.encode("utf-8")).hexdigest()
    print(dd)
    proxy = Proxy()
    dd = "9天 12小时 19分钟 57秒"
    proxy.aliveminute = dd
    print(proxy.aliveminute)
    