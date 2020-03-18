# coding:utf-8
'''
Created on 2020��3��8��

@author: cmck
'''

"""
function : 泥马IP代理站点的爬虫(http://www.nimadaili.com)
"""

import os
from bs4 import BeautifulSoup
from plugin import setting
import requests
import time
import traceback
from main.loghandle import LogHandler as mylogger
import random

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging
logging.getLogger("requests").setLevel(logging.WARNING)

threadlog = mylogger()


httpheader = {
    "Host": "www.nimadaili.com",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Referer": None,
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-CN,zh;q=0.9",
"Cookie": None
}


# 内容页
def singleproxy(proxyurl, header):
    for i in range(3):
        try:
            req = requests.get(url = proxyurl, headers = header, timeout = setting.timeout, verify = False)
  
            if req.status_code == 200:
                if req.text is not None:
                    #req.encoding = req.apparent_encoding
                    #req.encoding = "GB2312"
                    soup = BeautifulSoup(req.text, "html.parser")
                    trs = soup.findAll("tr")
                    
                    for tr in trs:
                        try:
                            if len(tr.contents) <= 1:
                                continue
                            
                            if tr.contents[1].name == "th":
                                continue
                            
                            tds = tr.findAll("td")
                            if len(tds) >= 6:
                                
                                ip = tds[0].text.split(":")[0]
                                port = tds[0].text.split(":")[1]
                                
                                annoy = tds[2].text.replace("代理", "")
                                
                                proxytype = tds[1].text.replace("代理", "")
                                
                                location = tds[3].text
                                if location.find("_") > -1:
                                    location = location.split("_")[1]
                                    
                                resptim = tds[4].text
                                verfi = tds[5].text
                            
                                proxy = setting.tmp_proxy.copy()
                                proxy["ipaddress"] = ip
                                proxy["port"] = port
                                proxy["svradd"] = location
                                proxy["prototype"] = proxytype
                                proxy["isanony"] = annoy
                                proxy["speed"] = resptim
                                proxy["availidtime"] = verfi
                            
                                yield proxy
                        except Exception:
                            threadlog.error(traceback.format_exc())
                            continue
                    return
                
            time.sleep(random.randint(0,5))
        except Exception:
            threadlog.error(traceback.format_exc())
            continue    
    
    return




def run():
    httpheader["User-Agent"] = setting.getua()
    preurl = "http://www.nimadaili.com"
    
    cookie = setting.getcookie(preurl, httpheader)
    
    iter = 0
    while cookie is None and iter < 10:
        cookie = setting.getcookie(preurl, httpheader)
        iter += 1
    
    httpheader["Cookie"] = "; ".join(key + "=" + value for (key, value) in cookie.items())
    
    proxylsurl = ["http://www.nimadaili.com/gaoni/","http://www.nimadaili.com/http/","http://www.nimadaili.com/https/"]
    #proxylsurl = ["http://www.nimadaili.com/gaoni/"]
    
    for proxyurl in proxylsurl:
        for i in range(0, setting.pagerange):
            httpheader["Referer"] = preurl
            topurl = proxyurl + str(i + 1)
            time.sleep(setting.rate)
            threadlog.info(os.path.split(__file__)[1] + " processing " + topurl)
            for proxy in singleproxy(topurl, httpheader):
                yield proxy 
    
            preurl = topurl


if __name__ == "__main__":
    proxies = run()
    for proxy in proxies:
        print(proxy)

