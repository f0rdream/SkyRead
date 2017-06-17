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


def send_message(phone_number):
    """
    通过POST 请求 requestSmsCode API 发送验证码到指定手机
    :param phone_number:手机号码
    :return:
    """
    reply = {}
    data = {
        "mobilePhoneNumber": phone_number,
        'op': '绑定手机号码'
    }
    r = requests.post(REQUEST_SMS_CODE_URL, data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        reply['status'] = 'success'
    else:
        reply['status'] = 'fail'
    return reply


def verify(phone_number,code):
    """
    发送 POST 请求到 verifySmsCode API 获取校验结果
    :param phone_number: 通过网页表单获取的电话号
    :param code: 通过网页表单获取的验证码
    :return:
    """
    # 把用户填写的电话号码和验证码构造成校验的URL
    verify_url = VERIFY_SMS_CODE_URL+"%s?mobilePhoneNumber=%s" % (code, phone_number)

    r = requests.post(verify_url,headers=headers)
    print r.status_code
    if r.status_code == 200:
        return True
    else:
        return False

