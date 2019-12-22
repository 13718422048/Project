#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/8
"""

import pymongo


class CMongodbclient(object):
	
	def __init__(self, name, host, port, **kwargs):
		self.tablename = kwargs["name"]
		self.client = pymongo.MongoClient(host, port, **kwargs)
		self.db = self.client.porxy
	
	def changetable(self, tablename):
		self.tablename = tablename
	
	def get(self, proxy):
		pass
	
	def put(self, proxy):
		pass
	
	def modify(self, proxy):
		pass
	
	def delete(self, proxy):
		pass