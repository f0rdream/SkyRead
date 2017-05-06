# coding:utf-8
# 爬取豆瓣用户读书详细数据
import requests
def get_headers():
    """
    登录用的代理头
    :return: get_headers()
    """
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Host':'www.zhihu.com',
        'Cookie':'gr_user_id=0a7ad251-56dc-491f-94bc-9b81b4c1817c; ll="118254"; bid=e41VRkK6zpA; ct=y; viewed="26704403_26957760_20432061_26980766_26925834_26943204_1082154_26948175_10548379_1230815"; ps=y; __utmt_douban=1; ap=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=903dc1b7-9782-42b1-aabd-0a65adb80e48; gr_cs1_903dc1b7-9782-42b1-aabd-0a65adb80e48=user_id%3A1; _vwo_uuid_v2=4AF75534E01ADDD8F0A9BA2AB2D9D67F|019654e26230cb2a7a9010e66407d0dd; __utmt=1; dbcl2="142806328:qhd0zH+eFVw"; ck=LZwF; push_noty_num=0; push_doumail_num=0; __utma=30149280.1553370323.1456817677.1493731170.1493788425.124; __utmb=30149280.14.5.1493788425; __utmc=30149280; __utmz=30149280.1493562569.118.65.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.14280',
        'Upgrade-Insecure-Requests':'1'
        ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        }
    return headers
login_url = "https://accounts.douban.com/login"
session = requests.session()
r = session.get('https://book.douban.com/')
print r.status_code
login_data = {
    'ck':'bndw',
    'form_email': '15071499956',
    'form_password':'867581452',
    'remember': 'on',
    'source': 'book',
    'redir': 'https://www.douban.com',
}
s = session.post(login_url, data=login_data, headers=get_headers(), verify=False)
# print s.status_code