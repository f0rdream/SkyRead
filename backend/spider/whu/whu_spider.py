# -*- coding: utf-8 -*-
# 武大图书馆爬虫  借阅数目 常常一起被借阅的书籍
import requests
from bs4 import BeautifulSoup as bs
isbn13 = "9787535732309"
# 9787535732309 时间简史
def get_response(url):
      response = requests.get(url)
      if response.status_code == 200:
            return response.text
      else:
            return ""
api = "http://opac.lib.whu.edu.cn/F/MR679AGD6RKJ1XXDEQ3UGQCYFNHVPQAG41S3935FS4MA1BRF6U-23102?func=find-b&adjacent=Y&find_code=ISB&request="+isbn13+\
      "&x=65&y=9&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="
print api
response = requests.get(api)
main_soup = bs(response.text,"lxml")

tabcontent = main_soup.find_all(attrs={'class':'tabcontent'})
print len(tabcontent)
detail2 = tabcontent[0]  # 第一个就是
href = detail2.find_all('tr')[-5].find_all('a')[0].get('href')  # 所有单册的链接
def get_detail(href):
      html = get_response(href)
      soup = bs(html,"lxml")
      table= soup.find_all('center')[0].find_all('table')
      detail =  table[6] # 借阅详情的表格
      tr = detail.find_all('tr')
      print len(tr)
      for i in range(1,24):
            td = tr[i].find_all('td')
            status = td[2].text.encode('latin1')# 单册状态,已借出或者外借书
            return_date = td[3].text.encode('latin1')  # 归还日期,20170313/20170311 或者在架上
            return_time = td[4].text.encode('latin1')# 归还时间 10:00
            location = td[5].text.encode('latin1')# 馆藏位置
            book_number = td[6].text.encode('utf-8')  # 索书号
            req_number = td[7].text.encode('utf-8')  # 请求数目
            bar_code = td[8].text.encode('utf-8')  # 条形码
            print status,return_date,return_time,location,book_number,req_number,bar_code
            #decode('latin1').encode('utf8')

# 全部重写,加入登录模块




