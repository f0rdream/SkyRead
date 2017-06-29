# coding:utf-8
# 查询补全部分
import time
from get_isbn import get_book_isbn
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
import requests
from bs4 import BeautifulSoup as bs
import MySQLdb
import time

global count
global id  # 豆瓣id,用来爬评论
global isbn13 # 校验码正确的isbn编号,用来爬藏书量和位置
global img_id # 豆瓣图片id

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0'
    , 'Upgrade-Insecure-Requests': '1'
    ,
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
           }

conn = MySQLdb.Connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = '1234',
    db = 'softcup',
    charset = 'utf8'
)


def db_set_ok(book_isbn,code):
    global conn
    try:
        conn.ping()
    except:
        conn = MySQLdb.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='1234',
            db='softcup',
            charset='utf8'
        )
    if code == 1:
        cursor = conn.cursor()
        sql = 'insert into check_400 values(%s,"1","0")' % book_isbn
        cursor.execute(sql)
        conn.commit()
        conn.close()
    else:
        cursor = conn.cursor()
        sql = 'insert into check_400 values(%s,"1","1")' % book_isbn
        cursor.execute(sql)
        conn.commit()
        conn.close()


def entry(key):
    global headers
    # api = "https://book.douban.com/subject_search?search_text="
    api = 'https://book.douban.com/subject_search?search_text='
    req_api = api+key
    try:
        req = requests.get(req_api,headers=headers,timeout=2,verify=True)
        req.encoding = 'utf-8'
        global conn
        if req.status_code == 200:
            handler(key,req.text)
            # db_set_ok(book_isbn,1)
            time.sleep(1)
            # 设置校验数据库为true
        elif req.status_code == 404:
            with open('log.txt','a') as l:
                l.write(book_isbn+"404 not found"+"\n")
                l.close()
            # 设置校验数据库为true
        elif req.status_code == 400 or req.status_code == 403:
            with open('log.txt','a') as l:
                l.write("代理被封了11111111111111111111111111111正在更换代理"+"\n")
                l.close()
            entry(book_isbn)
        else:
            with open('log.txt', 'a') as l:
                l.write(str(req.status_code)+str(book_isbn) + "爬取失败"+"\n")
                l.close()
            entry(book_isbn)
    except Exception as e:
        with open('log.txt', 'a') as l:
            l.write(str(e.message) +"出现了一些问题"+"\n")
            l.close()
        entry(key)


def handler(book_isbn,text):
    main_soup = bs(text,'lxml')
    try:
        book_url = main_soup.find_all(attrs={'class':'info'})[0].find('a').get('href')
        print book_url
        get_html(book_url,book_isbn)
    except:
        with open('log.txt', 'a') as l:
            l.write( book_isbn + "404 not found"+"\n")
            l.close()
        pass


def get_html(book_url,book_isbn):
    try:
        req = requests.get(book_url,timeout=2,headers=headers,verify=True)
        req.encoding = 'utf-8'
        status_code = req.status_code
        if status_code == 200:
            html = req.text
            parser(html,book_url)
            # db_set_ok(book_isbn, 2)
            # 设置数据库解析成功
        elif status_code == 400 or status_code == 403:
            with open('log.txt','a') as l:
                l.write("代理被封了正在更换代理"+"\n")
                l.close()
            get_html(book_url,book_isbn)
        else:
            with open('log.txt','a') as l:
                l.write("代理被封了正在更换代理"+"\n")
                l.close()
            get_html(book_url, book_isbn)
    except Exception as e:
        with open('log.txt', 'a') as l:
            l.write(str(e.message) +"出现了一些问题"+"\n")
            l.close()
        get_html(book_url, book_isbn)


def parser(html,book_url):
    main_soup = bs(html,'lxml')
    info_list = main_soup.find_all(attrs={'id': 'info'})
    d_id = book_url.split('/')[-2]
    author = ""
    tag = ""
    isbn13 = "",
    numRaters = "",
    average = "",
    subtitle = "",
    pubdate = "",
    origin_title = "",
    bingding = "",
    catalog = "",
    pages = "",
    publisher = "",
    title = "",
    summary = "",
    author_intro = ""
    price = ""
    img_id = ""
    if len(info_list) != 0:
        info = info_list[0].text.encode('utf-8')
        try:
            author_list = info.split('出版社')[0].strip().split('/')
            author_number = len(author_list)
            for i in range(0, author_number):
                if i == 0:
                    author += '&' + author_list[i].split('作者:')[1].split('\n')[2].strip()  # 第一作者
                else:
                    author += '&' + author_list[i].strip() + '&'
        except:
            pass
        try:
            isbn13 = info.split('ISBN:')[1].split('\n')[0].strip()
            print isbn13

        except:
            pass
        try:
            publisher = info.split('出版社:')[1].split('\n')[0].strip()
        except:
            pass
        try:
            pubdate = info.split('出版年:')[1].split('\n')[0].strip()
        except:
            pass
        try:
            pages = info.split('页数:')[1].split('\n')[0].strip()
        except:
            pass
        try:
            price = info.split('定价:')[1].split('\n')[0].strip()
        except:
            pass
        try:
            bingding = info.split('装帧:')[1].split('\n')[0].strip()
        except:
            pass
        try:
            origin_title = info.split('原作名:')[1].split('\n')[0].strip()
        except:
            pass
        try:
            subtitle = info.split('副标题:')[1].split('\n')[0].strip()
        except:
            pass

    else:
        with open('info_fail.txt', 'a') as i:
            i.write(d_id)
    try:
        dir_id = ("dir_" + d_id + "_full").encode('utf-8')
        catalog = main_soup.find_all(attrs={'id': dir_id})[0].text.replace('<br/>', '').replace(' ', '')
    except Exception as e:
        pass
    try:
        rate = main_soup.find_all(attrs={'class': 'rating_self clearfix'})[0]
        average = rate.find_all(attrs={'class': 'll rating_num '})[0].text
        numRaters = rate.find_all(attrs={'class': 'rating_people'})[0].text.encode('utf-8').split('人评价')[0]
    except:
        pass
    try:
        sum = main_soup.find_all(attrs={'id': 'link-report'})[0]
        try:
            short = sum.find_all(attrs={'class': 'intro'})[0].text.strip()
            summary = short
        except:
            pass
        try:
            all = sum.find_all(attrs={'class': 'intro'})[1].text.strip()
            summary = all
        except:
            pass
    except:
        pass
    try:
        tags = main_soup.find_all(attrs={"id": "db-tags-section"})[0].find_all(attrs={'class': 'indent'})[0].find_all(
            'span')
        for i in range(0, len(tags)):
            tag += "&" + tags[i].text.strip()
    except:
        pass
    try:
        title = main_soup.find_all(attrs={'property': 'v:itemreviewed'})[0].text
    except:
        pass
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
    except:
        pass
    try:
        img_id = main_soup.find_all(attrs={'class': 'nbg'})[0].get('href').split('/')[-1]
    except:
        pass
    # 先检查数据库连接情况
    global conn
    try:
        conn.ping()
    except:
        conn = MySQLdb.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='1234',
            db='softcup',
            charset='utf8'
        )
    cursor = conn.cursor()
    #sql = 'insert into book_info values("test","aaass","","","","","","","","","","","","","","","","","");'
    sql = 'insert into douban_p202 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql,(str(isbn13),str(numRaters),str(average),
                            str(subtitle),str(author),str(pubdate),
                            str(origin_title),str(img_id),str(bingding),
                            str(tag),str(catalog),str(pages),
                            str(d_id),str(publisher),str(title),
                            str(summary),str(author_intro),
                            str(price)))
    except Exception as e:
        print e
    conn.commit()
    conn.close()
    with open('log.txt', 'a') as l:
        l.write(str(isbn13) +"insert into database success===================================================================================成功"+"\n")
        l.close()
    print


class Spider():
    isbn_dict = []

    def get_isbn(self):
        dict = [202]
        self.isbn_dict = get_book_isbn(dict,0,100000)
    def spider(self):
        self.get_isbn()
        for isbn in self.isbn_dict:
            entry(isbn)
spider = Spider()
spider.spider()
