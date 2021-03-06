# coding:UTF-8
# 亚马逊图书爬虫
# 评分,热门评论
import urllib
import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 连接数据库
import MySQLdb


class AmazonSpider():
    book_link = None
    keyword = None
    average = None
    edit_recommendation = None
    famous_recommendation = None
    media_recommendation = None
    home_content = None
    soup = None
    isbn13 = None
    commentlist = None
    hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {'UserAgent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

    def get_book_link(self):
        api = "https://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Dstripbooks&field-keywords="
        urlword= urllib.quote(self.keyword)
        request_url = api + urlword
        hp_req = requests.get(request_url)
        main_soup = bs(hp_req.text,"lxml")
        resultCol = main_soup.find_all(attrs={'id':'resultsCol'})[0]
        result_0 = resultCol.find_all(attrs={'id':'atfResults'})[0].find_all('li',id='result_0')[0]
        book_link = result_0.find_all(attrs={'class':'a-column a-span12 a-text-center'})[0].find_all('a')[0].get('href')
        self.book_link = book_link

    def get_content(self):
        book_link = self.book_link
        try:
            self.home_content = requests.get(book_link,
                                             headers=self.hds[np.random.randint(0,len(self.hds))],
                                             timeout=2).text
        except Exception as e:
            print e.message
            print "timeout"
    def get_average(self):
        content = self.home_content
        self.soup = bs(content,'lxml')
        average_reviews = self.soup.find_all(attrs={'id': 'averageCustomerReviews'})
        average_span = average_reviews[0].find_all(attrs={'id': 'acrPopover'})[0]
        self.average = average_span.get('title').split('星')[0].split('平均')[1]
        print self.average

    def get_commendation(self,title):
        soup = self.soup
        content_0 = soup.find_all(attrs={'id': 's_content_0'})[0]
        content_1 = soup.find_all(attrs={'id': 's_content_1'})[0]
        if content_0.h3.text == '编辑推荐':
            self.edit_recommendation = content_0.text.strip().replace(' ','').replace('\n','')
            if content_1.h3.text == '名人推荐':
                self.famous_recommendation = content_1.text.strip().replace(' ','').replace('\n','')
            elif content_1.h3.text == '媒体推荐':
                self.media_recommendation = content_1.text.split('媒体推荐')[1].strip().replace(' ','').replace('\n','')
        elif content_0.h3.text == '名人推荐':
            self.famous_recommendation = content_0.text.strip().replace(' ','').replace('\n','')
            if content_1.h3.text == '媒体推荐':
                self.media_recommendation = content_1.text.strip().replace(' ','').replace('\n','')
        elif content_0.h3.text == '媒体推荐':
            self.media_recommendation = content_0.text.strip().replace(' ','').replace('\n','')
        else:
            print "No commendation"

        conn = MySQLdb.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='d1',
            charset='utf8'
        )
        cursor = conn.cursor()
        sql = 'insert into ama_info values(%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (str(title),str(self.isbn13),str(self.average), str(self.edit_recommendation),
                                 str(self.famous_recommendation),str(self.media_recommendation),
                                 ))
            conn.commit()
            conn.close()
        except Exception as e:
            print e
    def get_comment(self):
        soup = self.soup
        comments = soup.find_all(attrs={'class':'a-section celwidget'})
        conn = MySQLdb.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='d1',
            charset='utf8'
        )
        cursor = conn.cursor()
        for i in range(0,len(comments)):
            comment = comments[i].find_all(
                attrs={'class':'a-row a-spacing-small'})[0].find_all(
                 attrs={'class':'a-section'})[0].text.strip()
            sql = 'insert into ama_comment values (%s,%s)'
            print comment
            try:
                cursor.execute(sql, (str(self.isbn13),str(comment)))
            except Exception as e:
                print e
        conn.commit()
        conn.close()
    def spider(self,keyword,isbn13):
        self.keyword = keyword
        self.isbn13 = isbn13
        try:
            self.get_book_link()
            try:
                self.get_content()
                print "get content"
            except:
                pass
            try:
                self.get_average()
            except:
                pass
            try:
                self.get_commendation(keyword)
            except:
                pass
            try:
                self.get_comment()
            except:
                pass
        except:
            print "can't find this book"
        print str(self.isbn13)+"success"

