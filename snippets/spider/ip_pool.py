
# -*- coding: utf-8 -*-
import re
import time
import csv
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

# 构建ip pool-可用的ip池
def get_ip():
    url = 'http://www.xicidaili.com/nn'
    my_headers = {
        'Accept': 'text/html, application/xhtml+xml, application/xml;',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer': 'http: // www.xicidaili.com/nn',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 45.0.2454.101Safari / 537.36'
    }
    r = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(r.text,'html.parser')
    data = soup.find_all('td')
    ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  #匹配IP
    port_compile = re.compile(r'<td>(\d+)</td>')  #匹配端口
    ip = re.findall(ip_compile,str(data))    #获取所有IP
    port = re.findall(port_compile,str(data))  #获取所有端口
    ip_pool = [':'.join(i) for i in zip(ip,port)]  #列表生成式
    #组合IP和端
    print (ip_pool)
    return ip_pool

def test(proxy):
   try:
       response=requests.get('http://www.bilibili.com',proxies=proxy,timeout=2)
       if response:
           return proxy
   except:
       pass




if __name__=='__main__':
    proxy=getProxy()
    IPPool1=[]
    time1=time.time()
    for item in proxy:
        IPPool1.append(test(item))
    time2=time.time()
    print 'singleprocess needs '+str(time2-time1)+' s'
    pool=Pool()
    IPPool2=[]
    temp=[]
    time3=time.time()
    for item in proxy:
        temp.append(pool.apply_async(test,args=(item,)))
    pool.close()
    pool.join()
    for item in temp:
        IPPool2.append(item.get())
    time4=time.time()
    print 'multiprocess needs '+str(time4-time3)+' s'
