# coding:utf-8
from django.contrib.auth.models import User
from django.db import models


class UserRecommendList(models.Model):
    """
    存储用户的推荐列表
    """
    user = models.OneToOneField(User)
    isbn13_list = models.TextField()
    user_like = models.TextField(default=None)