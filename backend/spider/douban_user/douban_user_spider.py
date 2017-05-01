# coding:utf-8
# 爬取豆瓣用户读书详细数据
import requests
def get_headers():
    """
    登录用的代理头
    :return: get_headers()
    """
    headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0'
        ,'Host':'www.zhihu.com'
        ,'Upgrade-Insecure-Requests':'1'
        ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        }
    return headers
login_url = "https://accounts.douban.com/login"
session = requests.session()
r = session.get('https://book.douban.com/')
print r.status_code
login_data = {
    'form_email': '15071499956',
    'form_password':'867581452',
    'remember': 'on',
    'source': 'book',
    'redir': 'https://book.douban.com/',
}
# s = session.post(login_url, data=login_data, headers=get_headers(), verify=False)
# print s.status_code