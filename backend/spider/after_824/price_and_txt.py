#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 17-8-24 下午4:44
@Author  : TangZongYu
@Desc    : 电子书和书籍价格的爬虫
"""
import requests
from bs4 import  BeautifulSoup as bs


def l_book_price(isbn13):
    """
    利用朗朗比价网得到各个渠道的价格和链接
    """
    search_url = "http://www.langlang.cc/SearchAll.aspx?c=01&kwd=" + isbn13
    response = requests.get(search_url).text
    search_page = bs(response,"lxml")
    # print search_page.prettify()
    href_div = search_page.find_all(attrs={'class':'list_r_list_book'})
    href = href_div[0].find_all('a')[0].get("href")
    print href
    price_page = bs(requests.get(href).text,"lxml")
    price_table = price_page.find_all(attrs={'class':'deals'})[0].find_all("tr")
    print len(price_table)


def book_price(isbn13):
    """
    利用比价网得到各个渠道的价格和链接
    """
    search_url = "http://www.yaobijia.com.cn/search.aspx?kwd=" + isbn13
    s = requests.session()
    s.keep_alive = False
    response = requests.get(search_url)
    search_page = bs(response.text, "lxml")
    response.close()
    # print search_page.prettify()
    href_div = search_page.find_all(attrs={'class':'s_lan'})[0].find_all("a")[0]
    href = "http://www.yaobijia.com.cn" + href_div.get("href")
    price_page = bs(requests.get(href).text,"lxml")
    # 查找存有加密链接的script
    href_script = price_page.find_all(attrs={'language':'JavaScript'})[3].text
    # print href_script
    row_list = href_script.split("\n")
    for row in row_list:
        print row
        # print "------------------------"
    price_tr = price_page.find_all(attrs={'class':'deals'})[0].find_all(attrs={'class':'imgCell'})
    # for row in price_tr:
    #     td = row.find("td",width="160")
    #     price = td.find("span").text
    #     source = td.find(attrs={'class':'merptype'}).text
    #     print source
    #     origin_href = row.find(attrs={'class':'trustArea'}).find("a").get("href")
    #     print origin_href


book_price("9787111537403")
