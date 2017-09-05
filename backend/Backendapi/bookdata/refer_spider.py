#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 17-9-5 上午10:34
@Author  : TangZongYu
@Desc    : 
"""
# 9.4加入爬虫

import requests
import time
from bs4 import BeautifulSoup as bs
from models import Book
import MySQLdb
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0'
    , 'Upgrade-Insecure-Requests': '1'
    ,
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
           }


def refer_book(isbn13):
    """
    爬取一本书的相关书籍的id
    :param main_soup: 请求书籍的解析
    :param id: 书籍id
    :return:
    """
    try:
        book = Book.objects.get(isbn13=isbn13)
        id = book.d_id
    except Exception as e :
        print e
        return -1
    print "get_id"
    api = "https://book.douban.com/subject/" + id
    response = requests.get(api, headers=headers)
    if response.status_code == 200:
        main_soup = bs(response.text, "lxml")
        r_id = list()
        try:
            rec_section = main_soup.find_all(attrs={'id':'db-rec-section'})[0]
            dl = rec_section.find_all('dl')
            dl_num =  len(dl)  # 第六个是clear,第十二个是clear
            if dl_num <= 5:
                for i in range(0,dl_num):
                    refer_id = dl[i].find_all('dd')[0].find('a')['href'].split('/')[-2]
                    r_id.append(refer_id)
            elif dl_num > 5:
                for i in range(0,dl_num):
                    if i == 5:
                        pass
                    elif i > 10:
                        pass
                    else:
                        refer_id = dl[i].find_all('dd')[0].find('a')['href'].split('/')[-2]
                        r_id.append(refer_id)
            return r_id
        except Exception as e:
            print e
            print isbn13 +"no refer book"
            return -1