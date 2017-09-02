# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from bookdata.models import Book


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
    money = models.IntegerField(default=1000000)
    return_message = models.BooleanField(default=True)
    order_message = models.BooleanField(default=True)
    recommend_times = models.IntegerField(default=1)

    def __unicode__(self):
            return self.phone_number


class FeedBack(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    back_state = models.IntegerField(default=0)
    back_content = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)


class StarList(models.Model):
    """
    存储用户自建的首页分类
    """
    user = models.ForeignKey(User)
    list_type = models.IntegerField(default=0)  # 0为label,1为用户书单
    key_word = models.CharField(max_length=1000)  # 关键字
    user_list_id = models.IntegerField(default=-1)


class UserCreateBookList(models.Model):
    """
    用户自己建立的书单
    """
    user = models.ForeignKey(User)
    title = models.CharField(max_length=1000)
    img_id = models.CharField(max_length=300, default="--")
    comment = models.TextField()


class BookInList(models.Model):
    book_list = models.ForeignKey(UserCreateBookList)
    book = models.ForeignKey(Book)


class StarBookList(models.Model):
    """
    收藏的书单
    """
    user = models.ForeignKey(User)
    book_list = models.ForeignKey(UserCreateBookList)



