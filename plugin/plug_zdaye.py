#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/10/28
"""


# https://www.zdaye.com/dayProxy.html
# 站大爷网站爬虫


from bs4 import BeautifulSoup
import setting
import copy
import requests
import re
import time
'''from http import cookiejar
from urllib import request'''


httpheader = {
    "Host": "www.zdaye.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests" : "1",
    "User-Agent": "",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer" : "https://www.zdaye.com/dayProxy.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


	
# 单个列表页面
def proxylist(topurl, header):
	'''
	function: 获取单个页面上，各代理详情页的url
	paras: url, 单个代理页面的url
	return: <iter>
	'''
	
	#htmler = request.urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, cafile=None, capath=None, cadefault=False, context=None)
	
	req = requests.get(url = topurl, header = header, timeout = setting.timeout)
	if req.status_code == 200:
		soup = BeautifulSoup(req.text, "html.parser")
		hrefas = soup.findAll("a", href = re.compile(r'/dayProxy/ip/[0-9]+\.html'))
		for href in hrefas:
			yield href["href"]


# 内容页
def singleproxy(proxyurl, header):
	req = requests.get(url = proxyurl, header = header, timeout = setting.timeout)
	if req.status_code == 200:
		soup = BeautifulSoup(req.text, "html.parser")
		content = soup.find(name="div", class_ = "cont")
		proxys = content.split("<br>")
		if len(proxys) != 0:
			for i in range(len(proxys)):
				proxy = copy.deepcopy(setting.tmp_proxy)
				
				ipaddre, resource = proxys[i].split(" ")
				# ip
				res = re.findall("([0-9.]+)", ipaddre)
				if len(res) != 0:
					proxy["ipaddress"] = res[0]
				# port
				res = re.findall(":([0-9]+)@", ipaddre)
				if len(obj) != 0:
					proxy["port"] = res[0]
					
				# proto
				res = re.findall("@(\s)#", ipaddre)
				if len(res) != 0:
					proxy["prototype"] = res[0]
				
				# 匿名等级
				res = re.findall("[(\s)]", ipaddre)
				if len(res) != 0:
					proxy["isanony"] = res[0]
				
				res = re.findall("[(.+)$", ipaddre)
				if len(res) != 0:
					proxy["serveradd"] = res[0]
				
				yield proxy
	
# 翻页
def pagelist():
	
	pass

# 启动爬虫
def run():
	# 获取连接
	# 获取代理列表页面
	# 获取单个代理
	
	# page
	httpheader["User-Agent"] = setting.getua()
	
	cookie = setting.getcookie("https://www.zdaye.com/", httpheader)
	preurl = "https://www.zdaye.com/"
	
	httpheader["Cookie"] = "; ".join(key + "=" + value for key, value in cookie.iteritems())
	
	for i in range(0, setting.pagerange):
		
		httpheader["Referer"] = preurl
		if i == 0:
			# page=1时的操作
			topurl = "https://www.zdaye.com/dayProxy.html"
		else:
			topurl = "https://www.zdaye.com/dayProxy/{pagepos}.html".format(pagepos = i)
		
		for proxyurl in proxylist(topurl, httpheader):
			time.sleep(setting.rate)
			yield pagelist(proxyurl, httpheader)
		
		preurl = topurl
		


if __name__ == "__main__":
	
	url = "https://www.baidu.com"
	httpheader["Host"] = "www.baidu.com"
	
	httpheader["User-agent"] = setting.getua()
	# req = requests.get(url, headers = httpheader)
	cookies = setting.getcookie(url, httpheader)
	print(type(cookies))
	print(cookies)
	
	"""
	soup = BeautifulSoup(req.text, "html.parser")
	ls = soup.find("ul", attrs= {"id" : "cate_item"})
	#ls = soup.findAll("ul", id="cate_item")
	print(ls)
	#lss = list(ls.children)
	lss = ls.contents
	print(type(lss))
	
	for li in lss:
		print(type(li))
		print(li)
		print(li.a.string)
	
	
	for key,value in req.cookies.iteritems():
		print("{0}:{1}".format(key,value))
		"""
	print(req.cookies.items())
	