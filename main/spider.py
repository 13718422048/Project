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

# 多线程搜索代理网页，获取代理ip。
# 

# 动态加载库
import importlib
import sys

setting = importlib.reload(plugin.setting)


class CSpider(threading.Thread):
	
	def __init__(self, spidername, que):
		threading.Thread.__init__(self)
		self.__spidername = spidername
		self.__spider = None
		self.__que = que
	
	def run(self):
		if hasattr(setting, "pluginlist"):
			if self.__spidername in setting["pluginlist"]:
				# __import__: 搜索model
				try:
					self.__spider = getattr(__import__("plugin." + self.__spidername), self.__spidername)
				except Exception as e:
					traceback.print_exc()
		else:
			# TODO: 结束循环
			
			pass
					
	
		if self.__spider is not None:
			print(self.__spidername + " is running")
			proxylist = self.__spider.run()
			
			for proxy in proxylist:
				prox = Proxy()
				if isinstance(proxy, dict):
					
					try:
						prox.ipaddress = proxy["ipaddress"]
						prox.port =  proxy["port"]
						prox.serveradd =  proxy["serveradd"]
						prox.isanony =  proxy["isanony"]
						prox.prototype =  proxy["prototype"]
						prox.speed =  proxy["speed"]
						prox.conntime =  proxy["conntime"]
						prox.aliveminute =  proxy["aliveminute"]
						prox.availidtime =  proxy["availidtime"]
						self.__que.put(prox)
						
					except ValueError as e:
						#TODO: 
						traceback.print_exc()
						continue
					
				else:
					# TODO:
					pass
			
			# 爬过一次ip后，每天爬一次，每次只爬第一页
			setting.pagerange = 1
		
		else:
			# TODO:
			pass


# 
def run():
	if hasattr(setting, "pluginlist"):
		if isinstance(setting["pluginlist"], "list"):
			threadls = []
			que = queue.Queue()
			for spidplug in setting["pluginlist"]:
				thread = CSpider(spidplug, que)
				thread.start()
				threadls.append(thread)
			
			for thread in threadls:
				thread.join()
				
			while not que.empty():
				CDbopera.put(que.get())


if __name__ == "__main__":
	run()