# coding: utf-8


'''
function: 西刺代理
'''

import os
from bs4 import BeautifulSoup
import requests
import time
import copy
from plugin import setting
import traceback
from main.loghandle import LogHandler as mylogger
import random

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging
logging.getLogger("requests").setLevel(logging.WARNING)

threadlog = mylogger()

httpheader = {
    "Host" : "www.xicidaili.com",
    "User-Agent" : "",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding" : "gzip, deflate, br",
    "DNT" : "1",
    "Connection" : "keep-alive",
    "Cookie" : None,
    "Upgrade-Insecure-Requests" : "1",
    "If-None-Match" : "W/\"38bfd3249573a8d3b1ff9301bad1bdff"
}

# 需要获取If-None-Match

def extractlabel(soup, label , attr):
    try:
        
        trs = soup.findAll(label, _class = attr)
        
        for tr in trs:
            
            tds = list(tr.children)
            
            for pos, td in enumerate(tds):
                if td == "\n":
                    del tds[pos]
            
            if str(tds[0]).find("<th") != -1:
                continue
            
            ip = tds[1].string
            port = tds[2].string
            svradd = ""
            if len(tds[3].contents) > 1:
                if tds[3].contents[1].name == "a":
                    svradd = tds[3].a.string
                
            isannoy = tds[4].string
            prototype = tds[5].string 
            speed = (tds[6].find("div", class_ = "bar").get("title")).replace("秒", "")
            conntime = (tds[7].find("div", class_ = "bar").get("title")).replace("秒", "")
            livetime = tds[8].string
            validatime = "20" + tds[9].string
            
            yield (ip, port, svradd, isannoy, prototype, speed, conntime, livetime, validatime)
    except Exception:
        threadlog.error(traceback.format_exc())
        yield None

def getproxy(url, header):

    for i in range(3):
        
        try:
            res = requests.get(url, headers = header, verify = False, timeout = setting.timeout)

            if res.status_code == 200:
                if res.text is not None:
                
                    soup = BeautifulSoup(res.text, "html.parser")
                    
                    for attr in ["", "odd"]:
                        for cc in extractlabel(soup, "tr", attr):
                            
                            if cc is None:
                                continue
                            
                            proxy = copy.deepcopy(setting.tmp_proxy)
                            proxy["ipaddress"] = cc[0]
                            proxy["port"] = cc[1]
                            proxy["svradd"] = cc[2]
                            proxy["isanony"] = cc[3]
                            proxy["prototype"] = cc[4]
                            proxy["speed"] = cc[5]
                            proxy["conntime"] = cc[6]
                            proxy["aliveminute"] = cc[7]
                            proxy["availidtime"] = cc[8]
                        
                            yield proxy
                    return
                
            time.sleep(random.randint(0,5))    
        except Exception:
            threadlog.error(traceback.format_exc())
            continue           
    
    return
        
def run():    
    preurl = "https://www.xicidaili.com"
    # getcookie & getua
    proxyurl = ["https://www.xicidaili.com/nn/", "https://www.xicidaili.com/nt/", "https://www.xicidaili.com/wn/", "https://www.xicidaili.com/wt/"]
    #proxyurl = ["https://www.xicidaili.com/nn/"]
    
    
    httpheader["User-Agent"] = setting.getua()
    cookie = setting.getcookie(preurl, httpheader)
    
    iter = 0
    while cookie is None and iter < 10:
        cookie = setting.getcookie(preurl, httpheader)
        iter += 1
    
    httpheader["Cookie"] = "; ".join(k + "=" + val for (k, val) in cookie.items())
    
    for url in proxyurl:
        iterurl = ""
        for i in range(setting.pagerange):
            if i == 0:
                iterurl = url
            else:
                iterurl = url + str(i)
            
            time.sleep(setting.rate)
            
            threadlog.info(os.path.split(__file__)[1] + " processing " + iterurl)
            for proxy in getproxy(iterurl, httpheader):
                yield proxy

if __name__ == "__main__":
    
    for proxy in run():
        print(proxy)
    


