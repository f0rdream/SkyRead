# coding:utf-8
# 爬虫参数入口
import time
from get_isbn import get_book_isbn
from handler import entry
import MySQLdb
import json
import requests

# 请求的头部内容
headers = {
    "X-LC-Id": "SmuoKYDCgdwHsneB5bqbIzOE-gzGzoHsz",
    "X-LC-Key": "XapcSqtmlCbYg0PoEDUnrlbu",
    "Content-Type": "application/json",
}

# 请求发送验证码 API
REQUEST_SMS_CODE_URL = 'https://api.leancloud.cn/1.1/requestSmsCode'

# 请求校验验证码 API
VERIFY_SMS_CODE_URL = 'https://api.leancloud.cn/1.1/verifySmsCode/'

class Spider():
    isbn_dict = []

    def send_message(self):
        """
        通过POST 请求 requestSmsCode API 发送验证码到指定手机
        :param phone_number:手机号码
        :return:
        """
        data = {
            "mobilePhoneNumber": '15071499956',
            'op': '1号爬完了'
        }
        r = requests.post(REQUEST_SMS_CODE_URL, data=json.dumps(data), headers=headers)
    def get_isbn(self):
        self.isbn_dict = get_book_isbn('01',2071,3000)
    def spider(self):
        begintime = time.time()
        self.get_isbn()
        for isbn in self.isbn_dict:
            entry(isbn)
        endtime = time.time()
        self.send_message()
#         print "花去"+str(endtime-begintime)
spider = Spider()
spider.spider()
