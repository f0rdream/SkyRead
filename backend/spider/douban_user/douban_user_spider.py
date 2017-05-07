# coding:utf-8
# 爬取豆瓣用户读书详细数据
import requests
from bs4 import BeautifulSoup as bs
user_home = "https://book.douban.com/subject/1770782/comments/"
response = requests.get(user_home).text
soup = bs(response,"lxml")
comment_item = soup.find_all(attrs={'class':'comment-item'})


def get_book_item(href):
    response = requests.get(href).text
    # list view -> li -> item-show-title-href



for li in comment_item:
    avator =  li.find_all(attrs={'class':'avatar'})[0]
    username = avator.find_all('a')[0].get('title')
    href = avator.find_all('a')[0].get('href')+"collect?sort=time&start=0&filter=all&mode=list&tags_sort=count"
    print username,href
    get_book_item(href)