# coding:UTF-8
import json
import urllib

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
import hashlib

from rest_framework.permissions import AllowAny
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatpy.events import ScanCodeWaitMsgEvent
from wechatpy.enterprise import WeChatClient
from wechatpy.oauth import WeChatOAuth
from accounts.models import WeChatUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
# Create your views here.
from bookdata.models import  Book
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from sign import get_signature
from rest_framework.status import HTTP_200_OK
from newadmin.models import Admin_Permission
from serializers import PictureSerializer
from newadmin.models import Picture
@csrf_exempt
def wexin(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    WEIXIN_TOKEN = 'tangzongyu'
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("SkyRead")
    else:
        xml = request.body
        msg = parse_message(xml)
        if msg.type == 'text':
            # 加入关键词处理
            print msg.type
            if msg.content == u'你好' or msg.content == u'你是谁':
                content = "你好,这里是SkyRead"
            else:
                key = '8b005db5f57556fb96dfd98fbccfab84'
                api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
                request = api + str(msg.content)
                response = getHtml(request)
                dic_json = json.loads(response)
                content = dic_json['text']
            try:
                reply = TextReply(content=content,message=msg)
                r_xml = reply.render()
                openid = msg.source
                with open('openid.txt',"w") as f:
                    f.write(openid)
                return HttpResponse(r_xml)
            except Exception as e:
                reply = TextReply(content=str(e), message=msg)
                r_xml = reply.render()
                openid = msg.source
                with open('openid.txt', "w") as f:
                    f.write(openid)
                return HttpResponse(r_xml)
        elif msg.type == 'event':
            try:
                push = ScanCodeWaitMsgEvent(msg)
                content = msg.scan_result[7:]
                print content
                # 利用content找到书籍信息
                book = Book.objects.get(isbn13=content)
                title = book.title
                authors = book.author
                author = ' '
                if authors == '' or authors == '&':
                    return ' '
                else:
                    authors = authors.split('&')
                    for i in authors:
                        if i == '':
                            continue
                        else:
                            author += i + "/"
                price = book.price
                publisher = book.publisher
                if publisher == "('',)":
                    publisher = ' '
                summary = book.summary
                if summary == "('',)":
                    summary = ' '
                else:
                    summary = summary[0:200] + "......"
                book_info = title+"\n"+\
                            "作者:"+author+"\n"+\
                            "价格:"+price+"\n"+\
                            "出版社:"+publisher+"\n"+\
                            "内容简介:"+summary+"\n"+"----完整信息请进入应用主界面查看"
                reply = TextReply(content=book_info, message=msg)
                r_xml = reply.render()
                return HttpResponse(r_xml)
            except Exception as e:
                print e
                reply = TextReply(content="抱歉,暂时处理不了", message=msg)
                r_xml = reply.render()
                return HttpResponse(r_xml)
        else:
            reply = TextReply(content="抱歉,暂时处理不了", message=msg)
            r_xml = reply.render()
            return HttpResponse(r_xml)


@csrf_exempt
def auth(request):
    return HttpResponse('认证页面')


@csrf_exempt
def redict(request):
    # 本地模拟时候假设已经拿到数据
    id = "wx06e40e988b339f37"
    secret = "85a43e84aec7ea073877fab4349ee226"
    wechatouath = WeChatOAuth(id,secret,"redirect_uri=http://tangzongyu.com/redict",scope=u'snsapi_userinfo')
    code = request.GET.get('code')
    wechatouath.fetch_access_token(code)
    wechatouath.check_access_token()
    json_data = wechatouath.get_user_info()
    openid = json_data['openid']
    nickname = json_data['nickname']
    sex = json_data['sex']
    province = json_data['province']
    city = json_data['city']
    country = json_data['country']
    headimgurl = json_data['headimgurl']
    # openid = 'oYMTS0jjf2rhak6v6AxjC_nKl5hQ'
    # nickname = 'testuser'
    # sex = 1
    # province = '浙江'
    # city = '温州'
    # country = '中国'
    # headimgurl = 'http://wx.qlogo.cn/mmopen/dDqE5bg9gbZXkq2EOaHsnHRwN1xLiawElO4oKKfMvZYeFcf2U7yTvxHhIzkWCydiaVWh7xic5waUlw6daLtAxMEQCjRIKiaXWYjJ/0'
    try:
        wechat_user = WeChatUser.objects.get(openid=openid)
        user = authenticate(username=openid, password="pwd"+openid)
        if user is not None:
            if user.is_active:
                login(request, user)
                # response = HttpResponseRedirect('/homepage',status=200)
                # response.set_cookie()
                return render(request,'index.html')
            else:
                return HttpResponse('登录失败')
        else:
            return HttpResponse('登录失败')
    except:
        wechat_user = WeChatUser.objects.create(openid=openid, sex=sex, nickname=nickname, city=city,
                                                province=province, country=country, headimgurl=headimgurl)
        wechat_user.save()

        user = User.objects.create_user(username=openid, email='email', password="pwd" + openid)
        user.save()

        # 添加用户权限:
        admin_permission = Admin_Permission.objects.create(user=user)
        admin_permission.save()

        login_user = authenticate(username=openid, password="pwd" + openid)
        if login_user is not None:
            if login_user.is_active:
                login(request, login_user)
                return render(request, 'index.html')
            else:
                return HttpResponse('登录失败')
        else:
            return HttpResponse('登录失败')

@csrf_exempt
def test_page(request):
    openid = 'oYMTS0jjf2rhak6v6AxjC_nKl5hQ'
    nickname = 'testuser'
    sex = 1
    province = '浙江'
    city = '温州'
    country = '中国'
    headimgurl = 'http://wx.qlogo.cn/mmopen/dDqE5bg9gbZXkq2EOaHsnHRwN1xLiawElO4oKKfMvZYeFcf2U7yTvxHhIzkWCydiaVWh7xic5waUlw6daLtAxMEQCjRIKiaXWYjJ/0'
    try:
        wechat_user = WeChatUser.objects.get(openid=openid)
        user = authenticate(username=openid, password="pwd" + openid)
        if user is not None:
            if user.is_active:
                login(request, user)
                # response = HttpResponseRedirect('/homepage',status=200)
                # response.set_cookie()
                return render(request, 'index.html')
            else:
                return HttpResponse('登录失败')
        else:
            return HttpResponse('登录失败')
    except:
        wechat_user = WeChatUser.objects.create(openid=openid, sex=sex, nickname=nickname, city=city,
                                                province=province, country=country, headimgurl=headimgurl)
        wechat_user.save()
        user = User.objects.create_user(username=openid, email='email', password="pwd" + openid)
        user.save()
        login_user = authenticate(username=openid, password="pwd" + openid)
        if login_user is not None:
            if login_user.is_active:
                login(request, login_user)
                return render(request, 'index.html')
            else:
                return HttpResponse('登录失败')
        else:
            return HttpResponse('登录失败')

# 得到微信签名:


class Sign(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        url = self.request.GET.get("url")
        reply = get_signature(url)
        return Response(reply,HTTP_200_OK)


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


class PictureVIEW(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        picture = Picture.objects.all()
        serializer = PictureSerializer(picture,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


