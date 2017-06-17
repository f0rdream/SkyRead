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

    def __unicode__(self):
        return self.nickname

class PhoneUser(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=200,primary_key=True)
    email = models.CharField(max_length=200,default=None,blank=True,null=True)
    real_name = models.CharField(max_length=200,default=None,blank=True,null=True)
    def __unicode__(self):
            return self.phone_number


