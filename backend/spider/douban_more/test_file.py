# coding:utf-8
import requests
import time
from bs4 import BeautifulSoup as bs

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
def comments_spider(id):
    """
    爬取书籍的热门评论和最新评论
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
            print comment_vote,star,comment_time
    except Exception as e:
        print e
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

review_spider("1084336")