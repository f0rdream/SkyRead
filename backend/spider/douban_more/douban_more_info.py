# coding:UTF-8
# 豆瓣试读,短评,书评,目录,相关书籍爬虫
from timeit import timeit

import requests
import time
from bs4 import BeautifulSoup as bs

def author_intro_spider(main_soup):
    author_intro = ""
    try:
        a_intro = main_soup.find_all(attrs={'id': 'link-report'})[0].find_next_siblings(attrs={'class': 'indent'})[0]
        try:
            short = a_intro.find_all(attrs={'class': 'intro'})[0].text.strip()
            author_intro = short
        except:
            pass
        try:
            all = a_intro.find_all(attrs={'class': 'intro'})[1].text.strip()
            author_intro = all
        except:
            pass
        print author_intro
    except:
        pass


def douban_spider(id):
    """
    爬虫入口
    :param id: 书籍id
    :return:
    """
    begin_time = time.time()
    api = "https://book.douban.com/subject/"+id
    response = requests.get(api)
    if response.status_code == 200:
        main_soup = bs(response.text, "lxml")
        # 爬取作者简介,部分需要
        author_intro_spider(main_soup)
        # 爬取试读部分
        pre_reading_spider(main_soup,id)

        # 爬取短评论
        comments_spider(id)

        # 爬取书评,时间长
        review_spider(id)

        #爬取相关书籍
        refer_book(main_soup,id)
    else:
        print id + "页面抓取失败"
        print response.status_code
    end_time = time.time()
    print end_time-begin_time


def download_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return ""


def review_spider(id):
    """
    爬取书评
    :param id: 书籍id
    :return:
    """
    # 爬取书评,爬取时间较长
    try:
        begin_time = time.time()
        reviews_api = 'https://book.douban.com/subject/' + id + "/reviews"
        reviews_req = requests.get(reviews_api)
        if reviews_req.status_code == 200:
            review_soup = bs(reviews_req.text, "lxml")
            review_div = review_soup.find_all(attrs={'class': 'review-list'})[0].find_all('div', typeof='v:Review')
            number = len(review_div)
            if number > 5:
                for i in range(0, 5):
                    link = review_div[i].find_all(attrs={'class': 'title-link'})[0].get('href')
                    content = download_page(link)
                    time.sleep(0.5)
                    content_soup = bs(content, "lxml")
                    full_content = content_soup.find_all(attrs={'class': 'review-content clearfix'})[0].text
                    print full_content
                for i in range(5,number):
                    # 超过5条的存link
                    link = review_div[i].find_all(attrs={'class': 'title-link'})[0].get('href')
            else:
                for i in range(0, 5):
                    link = review_div[i].find_all(attrs={'class': 'title-link'})[0].get('href')
                    content = download_page(link)
                    content_soup = bs(content, "lxml")
                    full_content = content_soup.find_all(attrs={'class': 'review-content clearfix'})[0].text
                    print full_content
        else:
            print "请求书评失败"
        end_time = time.time()
        print end_time - begin_time
    except Exception as e:
        print e
        print id + "爬取书评失败"


def pre_reading_spider(main_soup,id):
    """
    爬取试读部分,大部分书籍没有这个版块
    :param response: 请求书籍主页的响应
    :param id: 书籍id
    :return:
    """
    try:
        pre_reading = main_soup.find_all(attrs={'class': 'col2-list clearfix'})
        if len(pre_reading) != 0:
            for i in range(0, len(pre_reading)):
                pre_reading_url = pre_reading[i].find_all('a')[0].get('href')
                parse_pre_reading(id,pre_reading_url)
        else:
            print id + " 没有试读部分"
    except Exception as e:
        print id + '爬取试读部分失败'
        print e


def parse_pre_reading(id,url):
    """书籍试读部分解析,存储
    :param id: 书籍id
    :param url: 试读url
    :return:
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.text,"lxml")
        try:
            content = soup.find_all(attrs={'id': 'content'})[0]
            title = content.find('h1').text.encode('utf-8')  # 试读的标题
            book_content = content.find_all(attrs={'class':'note'})[0].text.encode('utf-8')  # 试读的主体部分
            print title,id #试读标题
            print book_content  #试读内容
        except Exception as e:
            print e
    else:
        print "请求失败"


def comments_spider(id):
    """
    爬取书籍的热门评论20条
    :param main_soup: 请求书籍的解析
    :param id: 书籍id
    :return:
    """
    try:
        api = "https://book.douban.com/subject/"+id+"/comments/"
        response = requests.get(api)
        soup = bs(response.text,"lxml")
        comment = soup.find_all(attrs={'class':'comment-item'})
        for li in comment:
            comment_content = li.find('p', 'comment-content').text  # 评论具体内容
            comment_vote = li.find('span', 'vote-count').text  # 赞同数目
            comment_info = li.find_all('span', 'comment-info')  # 评价详情,时间和（很差,较差,还行,力荐,推荐)
            comment_star = comment_info[0].find_all('span')[0].get('title')
            if comment_star != None:
                star = get_star(comment_star)
                comment_time = comment_info[0].find_all('span')[1].text
            else:
                star = None
                comment_time = comment_info[0].find_all('span')[0].text
    except Exception as e:
        print e


def get_star(comment_star):
    """
    转换评价星级的原始数据
    :param comment_star: 原始数据
    :return:
    """
    if comment_star.encode('utf-8') == "很差":
        return 1
    elif comment_star.encode('utf-8') == "较差":
        return 2
    elif comment_star.encode('utf-8') == "还行":
        return 3
    elif comment_star.encode('utf-8') == "推荐":
        return 4
    elif comment_star.encode('utf-8') == "力荐":
        return 5
    else:
        return 0


def refer_book(main_soup, id):
    """
    爬取一本书的相关书籍的id
    :param main_soup: 请求书籍的解析
    :param id: 书籍id
    :return:
    """
    rec_section =  main_soup.find_all(attrs={'id':'db-rec-section'})[0]
    dl = rec_section.find_all('dl')
    dl_num =  len(dl)  # 第六个是clear,第十二个是clear
    if dl_num <= 5:
        for i in range(0,dl_num):
            refer_id = dl[i].find_all('dd')[0].find('a')['href'].split('/')[-2]
            print refer_id
    elif dl_num > 5:
        for i in range(0,dl_num):
            if i == 5:
                pass
            elif i > 10:
                pass
            else:
                refer_id = dl[i].find_all('dd')[0].find('a')['href'].split('/')[-2]
                print refer_id
begin_time = time.time()
douban_spider('1084336')
print time.time()-begin_time