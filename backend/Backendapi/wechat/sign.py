# coding:utf-8
import time
import random
import string
import hashlib
import requests
import json
from django.core.cache import cache

def get_access_token():
    api ="https://api.weixin.qq.com/cgi-bin/token?" \
         "grant_type=client_credential" \
         "&appid=wx06e40e988b339f37" \
         "&secret=85a43e84aec7ea073877fab4349ee226"
    response = requests.get(api)
    if response.status_code == 200:
        return response.json()['access_token']
# 在全局缓存jsapi_ticket


def get_ticket():
    """
    得到tickct
    :return:
    """
    cache_key = 'jsapi_ticket'
    ticket = cache.get(cache_key)
    if ticket:
        print "成功找到ticket缓存--------\n"+ticket
        return ticket
    else:
        api = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?" \
              "access_token="+get_access_token()+"&type=jsapi"
        response = requests.get(api)
        if response.status_code == 200:
            dict = json.loads(response.text)
            ticket = dict['ticket']
            cache.set('jsapi_ticket',ticket,6500)
            return ticket


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret


def get_signature(url):
    """
    得到签名,提供给接口
    :return:
    """
    sign = Sign(get_ticket(),url)
    return sign.sign()

# TODO 添加缓存
