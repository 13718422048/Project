#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/7
"""

import re
import hashlib

class Proxy:
	def __init__(self):
		# ip
		self.__ipaddress = ""
		# 端口
		self.__port = 0
		# ip所在地址
		self.__serveradd = ""
		# 匿名状态
		self.__isanony = 1
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
		# ip被使用频次，默认为10次。为零的ip不会再被取出。
		self.__frequency = 10
		
		# 随机生成一个哈希值，用于标识代理
		self.__proxyid = 0
		
	@property
	def proxyid(self):
		return self.__proxyid
	
	@property
	def ipaddress(self):
		return self.__ipaddress
	
	@property.setter
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
	
	@property.setter
	def port(self, port):
		if(type(port) == "str" and port.isdigit()):
			if(int(port) > 0 and int(port) < 65535):
				self.__port = port
			else:
				raise ValueError("该值不在0~65535之间")
		else:
			raise ValueError("该值不是数字")
				
	
	@property
	def serveradd(self):
		return self.__serveradd	
	
	@property.setter
	def serveradd(self, serveradd):
		self.__serveradd = serveradd
	
	@property
	def isanony(self):
		return self.__isanony		
	
	@property.setter
	def isanony(self, isanony):
		self.__isanony = isanony
	
	@property
	def prototype(self):
		return self.__prototype
	
	@property.setter
	def prototype(self, value):
		value = str(value).replace(" ", "")
		if value.lower() not in ["http", "https"]:
			self.__prototype = "http"
			
		else:
			self.__prototype = value
			
	@property
	def isanony(self):
		return self.__isanony

	@property.setter
	def isanony(self, value):
		value = str(value).replace(" ", "")
		annonytype = {
		    "透明" : 0,
		    "高匿" : 1,
		    "普匿" : 2,
		    "未知" : 3,
		    "" : 4
		        }
		self.__isanony = annonytype.get(value, None)
		if self.__isanony is None:
			raise ValueError("未确定类型")
		
	@property
	def aliveminute(self):
		return self.__aliveminute
	
	@property.setter
	def aliveminute(self, value):
		try:
			value = str(value).replace(" ", "")
			
			"""if value.find("天") > -1:
				self.__aliveminute = int(value.split("天")[0]) * 24 * 60
			
			elif value.find("分") > -1:
				self.__aliveminute = int(value.split("分")[0])
			else:
				raise ValueError("存活时间不确定")"""
		except ValueError as vale:
			raise ValueError("不确定时间")
			
	@property
	def frequency(self):
		return self.__frequency
	
	@property.setter
	def frequency(self, value):
		self.__frequency = value
	
	