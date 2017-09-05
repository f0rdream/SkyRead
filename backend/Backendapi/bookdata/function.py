# coding:utf-8
# 查询补全部分
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
import requests
from bs4 import BeautifulSoup as bs
import MySQLdb
import time
import base64

global count
global id  # 豆瓣id,用来爬评论
global isbn13 # 校验码正确的isbn编号,用来爬藏书量和位置
global img_id # 豆瓣图片id
from transfer_index import get_author_index,get_title_index
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
           }

conn = MySQLdb.Connect(
    host = 'tdsql-axy3u6tl.sh.cdb.myqcloud.com',
    port = 92,
    user = 'wangyang',
    passwd = 'skyread@614',
    db = 'skyread',
    charset = 'utf8'
)


def entry(key):
    global headers
    api = 'https://book.douban.com/subject_search?search_text='
    req_api = api+key
    try:
        req = requests.get(req_api,headers=headers,timeout=2,verify=True)
        req.encoding = 'utf-8'
        global conn
        if req.status_code == 200:
            isbn13 = handler(key,req.text)
            time.sleep(1)
            # 设置校验数据库为true
            return isbn13
        elif req.status_code == 404:
            pass
            # 设置校验数据库为true
    except Exception as e:
        pass


def handler(book_isbn,text):
    main_soup = bs(text,'lxml')
    try:
        book_url = main_soup.find_all(attrs={'class':'info'})[0].find('a').get('href')
        print book_url
        isbn13 = get_html(book_url,book_isbn)
        return isbn13
    except:
        pass


def get_html(book_url,book_isbn):
    try:
        req = requests.get(book_url,timeout=2,headers=headers,verify=True)
        req.encoding = 'utf-8'
        status_code = req.status_code
        if status_code == 200:
            html = req.text
            isbn13 = parser(html,book_url)
            return isbn13
        elif status_code == 400 or status_code == 403:
            pass
        else:
            pass
    except Exception as e:
        pass


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
        pass
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
            host='tdsql-axy3u6tl.sh.cdb.myqcloud.com',
            port=92,
            user='wangyang',
            passwd='skyread@614',
            db='skyread',
            charset='utf8'
        )
    cursor = conn.cursor()
    sql = 'insert into bookdata_book values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    author_for_index = get_author_index(author)
    title_for_index = get_title_index(title)

    try:
        cursor.execute(sql,(str(isbn13),str(numRaters),str(average),
                            str(subtitle),str(author),str(pubdate),
                            str(origin_title),str(img_id),str(bingding),
                            str(tag),str(catalog),str(pages),
                            str(d_id),str(publisher),str(title),
                            str(summary),str(author_intro),
                            str(price),str(0),str(title_for_index),str(author_for_index)))

    except Exception as e:
        print e
    conn.commit()
    conn.close()
    return str(isbn13)


def book_price(book_isbn13, title):
    """
    利用比价网得到各个渠道的价格和链接,加入用标题索引
    """
    try:
        search_url = "http://www.yaobijia.com.cn/search.aspx?kwd=" + book_isbn13
        s = requests.session()
        s.keep_alive = False
        response = requests.get(search_url)
        search_page = bs(response.text, "lxml")
        response.close()
        # print search_page.prettify()
        href_div = search_page.find_all(attrs={'class':'s_lan'})[0].find_all("a")[0]
        href = "http://www.yaobijia.com.cn" + href_div.get("href")
        price_page = bs(requests.get(href).text,"lxml")
        price_tr = price_page.find_all(attrs={'class': 'deals'})[0].find_all(attrs={'class': 'imgCell'})
        price_list = list()
        for row in price_tr:
            price_dict = dict()
            td = row.find("td",width="160")
            price = td.find("span").text
            source = td.find(attrs={'class':'merptype'}).text
            price_dict['price'] = price
            price_dict['source_name'] = source
            price_dict['source_url'] = search_url
            price_list.append(price_dict)
            print price_list
        return price_list
    except:
        search_url = "http://www.yaobijia.com.cn/search.aspx?kwd=" + title
        s = requests.session()
        s.keep_alive = False
        response = requests.get(search_url)
        search_page = bs(response.text, "lxml")
        response.close()
        # print search_page.prettify()
        href_div = search_page.find_all(attrs={'class': 's_lan'})[0].find_all("a")[0]
        href = "http://www.yaobijia.com.cn" + href_div.get("href")
        price_page = bs(requests.get(href).text, "lxml")
        price_tr = price_page.find_all(attrs={'class': 'deals'})[0].find_all(attrs={'class': 'imgCell'})
        price_list = list()
        for row in price_tr:
            price_dict = dict()
            td = row.find("td", width="160")
            price = td.find("span").text
            source = td.find(attrs={'class': 'merptype'}).text
            price_dict['price'] = price
            price_dict['source_name'] = source
            price_dict['source_url'] = search_url
            price_list.append(price_dict)
            print price_list
        return price_list

    # origin_href = row.find(attrs={'class':'trustArea'}).find("a").get("href")
    # print origin_href
    # 查找存有加密链接的script
    # href_script = price_page.find_all(attrs={'language':'JavaScript'})[3].text
    # print href_script
    # row_list = href_script.split("\n")
    # for row in row_list:
    #     print row


class BaiduOCR:
    def __init__(self):
        self.access_token = "24.08ab1f10f777a850579de1ec5c2d7f28.2592000.1506475995.282335-10044680"
        self.ocr_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s" % self.access_token
        return

    # 文字识别
    def img2text(self, filename):
        image_file = open(filename,"rb")
        base64_code = base64.b64encode(image_file.read())
        image_file.close()
        data = dict()
        data['image'] = base64_code
        result = requests.post(self.ocr_url, data=data,
                               headers={'Content-Type': 'application/x-www-form-urlencoded'})
        data_result = result.json()
        return data_result


def image_to_text(file_name):
    ocr = BaiduOCR()
    result = ocr.img2text(file_name)
    return result
