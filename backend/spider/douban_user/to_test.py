
# coding:utf-8
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
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
    # browser = webdriver.Firefox(firefox_profile=firefox_profile)
    browser = webdriver.PhantomJS()
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
    print user,item
# print(get_user_book())
get_book_item('https://book.douban.com/people/fugen/')
