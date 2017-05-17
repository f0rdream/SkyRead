# coding:utf-8
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

print(get_user_book('https://book.douban.com/people/fugen/'))