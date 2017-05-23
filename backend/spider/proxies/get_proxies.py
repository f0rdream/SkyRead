# coding:utf-8
import requests
import numpy as np
from multiprocessing.dummy import Pool as ThreadPool

import time


def get_proxies():
    api = "http://tvp.daxiangdaili.com/ip/?tid=556621659536931&num=20&foreign=none&filter=on"
    req = requests.get(api)
    result =  req.text.split('\r')
    number = len(result)
    IPpool = []
    for i in range(0,number):
        proxie = result[i].strip()
        IPpool.append(proxie)
    return IPpool

proxies = get_proxies()
def get_valid_proxies(proxies):
    hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
    test_proxies = 'http://lwons.com/wx'
    url = 'https://book.douban.com/subject_search?search_text=9787111123451'
    can_connect = False
    first_result = []
    results = []
    cur = 0
    for p in proxies:
        proxy = {
                 'https': 'https://' + p, }
        try:
            print proxy
            r = requests.get(test_proxies,proxies=proxy,timeout=1)
            if r.text == 'default':
                can_connect = True
        except Exception,e:
            print "error",e.message
            can_connect = False
        if can_connect:
            print '初步筛选',p
            first_result.append(p)
    for p in first_result:
        proxy = {
                 'https':'https://'+ p}
        print proxy
        succeed = False
        try:
            begin_time = time.time()
            r = requests.get(url, headers=hds[np.random.randint(0,len(hds))],proxies=proxy,timeout=2)
            end_time = time.time()
            if end_time- begin_time > 120:
                succeed = False
            elif r.status_code == 200:
                print r.text
                succeed = True
        except Exception, e:
            print 'error:', e.message
            succeed = False
        if succeed:
            print '验证成功:', p
            with open('douban_index.txt','a') as pro:
                pro.write(p)
                pro.write("\n")
                pro.close()
            results.append(p)
            cur += 1
        else:
            print '验证失败',p
    return results

if __name__ == '__main__':
    for i in range(0,5):
        results= get_valid_proxies(proxies)
        print str(i)+"次爬完-----------------------------------------------------分割线",
        print len(results)




