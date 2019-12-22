#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/8
"""


import os
import sys


class CDbopera(object):
	
	def __new__(self, cls):
		if not hasattr(cls,"_instance"):
			cls.instance = super(CDbopera, cls).__new__(cls)
			
		return cls.instance
	
	def __init__(self):
		pass
	
	@classmethod
	def query(self, key, **keys):
		pass 

	@classmethod
	def insert(self, proxy):
		pass

	@classmethod
	def modify(self, proxy):
		'''
		return -1 / 1
		异常抛出
		'''
		pass
	
	@classmethod
	def delete(self, ip, port, protocol):
		pass


# 增删改查










