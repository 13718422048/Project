#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/10
"""


import mysqlclient


class CMysqlClient(object):
	
	def __init__(self, *args, **kwargs):
		# 构造函数
		user = kwargs.get("user", d=None)
		password = kwargs.get("password", d=None)
		ip = kwargs.get("ip", None)
		database = kwargs.get("ip", None)
		
		pass
	
	def connect(self):
		"""
		连接数据库
		"""
		pass
	
	def 