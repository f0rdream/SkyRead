# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
class WeChatUser(models.Model):
    # user = models.OneToOneField(User, related_name="wechat_user")
    nickname = models.CharField(max_length=1000,default='')
    openid = models.CharField(max_length=1000,default='')
    sex = models.IntegerField(default=1)
    province = models.CharField(max_length=1000,default='')
    city = models.CharField(max_length=1000,default='')
    country = models.CharField(max_length=1000,default='')
    headimgurl = models.CharField(max_length=1000,default='')


