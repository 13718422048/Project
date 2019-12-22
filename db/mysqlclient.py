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
		self._conn = None
		pass
	
	def __conn(self, *args, **kwargs):
		__type = None
		
		if db_type == "mongodb":
			__type = "mongodb"
		
		if db_type == "mysql":
			__type = "mysql"
		
			
		pass
	
	
	
	def __def__(self):
		# 析构函数
		# 判断mysql是否连接，连接则关闭连接
		if self._conn:
			pass
		