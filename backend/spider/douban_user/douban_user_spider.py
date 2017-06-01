# coding:utf-8
# 爬取豆瓣用户读书详细数据
import urllib2

import MySQLdb
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time


def get_user_book(url):
    """
    通过评论的href得到这个用户最近读过的30本书籍的页面
    :param url:
    :return:
    """
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.download.folderList", 2)
    # firefox_profile.set_preference("permissions.default.stylesheet", 2)
    firefox_profile.set_preference("permissions.default.image", 2)
    firefox_profile.set_preference("javascript.enable", False)
    browser = webdriver.Firefox(firefox_profile=firefox_profile)
    # browser = webdriver.
    browser.get(url)
    browser.find_element_by_class_name('nav-list').find_element_by_xpath('./li[6]').click()
    time.sleep(2)  # 要足够的时间去跳转
    browser.find_element_by_class_name('grid-list-bar').find_element_by_xpath('./li[2]').click()
    time.sleep(2)
    html = browser.page_source
    browser.quit()
    return html



def get_book_item(href):
    """
    通过username,href得到这个用户最近读过的30本书籍
    :param username:
    :param href:
    :return:
    """
    html = get_user_book(href)
    soup = bs(html,'lxml')
    ul = soup.find_all(attrs={'class':'list-view'})[0]
    li = ul.find_all('li')
    user = href.split('/')[-2]
    item = ''
    for i in range(0,len(li)):
        item_href = li[i].find_all(attrs={'class':'title'})[0].find('a').get('href')
        item_id = item_href.split('/')[-2]
        # item_title = li[i].find_all(attrs={'class':'title'})[0].find('a').text.strip()
        item = item + item_id+'&'
    # 存入数据库
    conn = MySQLdb.Connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = '123456',
        db = 'douban_user',
        charset = 'utf8'
    )
    cursor = conn.cursor()
    sql = "insert into user_item values(%s,%s)"
    try:
        cursor.execute(sql, (str(user), str(item)))
        conn.commit()
        conn.close()
    except Exception as e:
        print e

def log(i):
    with open('log.txt','a') as l:
        l.write(str(i)+"success"+"\n")
        l.close()
def get_user_href(begin,end):
    """
    通过追风筝的人的评论详情爬取用户href
    :return:
    """
    count = 0
    for i in range(begin,end):
        print begin
        user_home = "https://book.douban.com/subject/1770782/comments/"+"hot?p="+str(i)
        response = urllib2.urlopen(user_home).read()
        soup = bs(response,"lxml")
        comment_item = soup.find_all(attrs={'class':'comment-item'})
        time.sleep(1)
        for li in comment_item:
            avator = li.find_all(attrs={'class':'avatar'})[0]
            user_id = avator.find_all('a')[0].get('href').split("/")[-2]
            href = "https://book.douban.com/people/" + user_id + "/"
            try:
                get_book_item(href)
                count +=1
                print str(count) + "========success"
            except:
                pass
        log(i)

a = time.time()
get_user_href(2000,2500)  # 500-560页码
print time.time() - a
