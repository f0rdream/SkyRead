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


class UserPosition(models.Model):
    """
    存储用户上次登录的坐标
    """
    user = models.OneToOneField(User)
    x_point = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    y_point = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)

