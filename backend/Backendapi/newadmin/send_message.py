# coding:utf-8
import requests,json
# 发送短信的请求头及其url
# 请求的头部内容
headers = {
    "X-LC-Id": "qfgW1gQUGDESnV1NvtnqkClo-gzGzoHsz",
    "X-LC-Key": "P7WiKSkgDxnbaDW0MulQ3WxI",
    "Content-Type": "application/json",
}

# 请求发送验证码 API
REQUEST_SMS_CODE_URL = 'https://api.leancloud.cn/1.1/requestSmsCode'
# 请求校验验证码 API
VERIFY_SMS_CODE_URL = 'https://api.leancloud.cn/1.1/verifySmsCode/'


def send_borrow_message(phone,name,time):
    """
    通过POST 请求 requestSmsCode API 发送验证码到指定手机
    :param phone_number:手机号码
    :return:
    """
    reply = {}
    data = {
        "mobilePhoneNumber": phone,
        "template":"borrow_message",
        "sign":"message",
        "book_title":name,
        "left_time":time,
    }
    r = requests.post(REQUEST_SMS_CODE_URL, data=json.dumps(data), headers=headers)
    print r.text
    print r.status_code
    if r.status_code == 200:
        reply['status'] = 'success'
    else:
        reply['status'] = 'fail'
    return reply


def get_access_token():
    api ="https://api.weixin.qq.com/cgi-bin/token?" \
         "grant_type=client_credential" \
         "&appid=wx06e40e988b339f37" \
         "&secret=85a43e84aec7ea073877fab4349ee226"
    response = requests.get(api)
    if response.status_code == 200:
        return response.json()['access_token']


def send_back_wechat(openid,name,time):
    api = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % \
          str(get_access_token())
    data = {
        "touser": openid,
        "template_id": "VW8YCdZgeGE-weHvd9D4Twt_HwQ-PxmmHrVwMhj5c_U",
        "topcolor": "#FF0000",
        "data": {
            "book_title":{
                "value": name,
                "color": "#DD2222"
            },
            "left_time": {
                "value": time,
                "color": "#DD2222"
            },
        }
    }
    r = requests.post(api, json.dumps(data))
    if r.status_code == 200:
        print "success"
    else:
        print "fail"
