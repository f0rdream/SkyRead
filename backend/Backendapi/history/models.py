#coding:utf-8
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class SearchHistory(models.Model):
    """
    搜索历史
    """
    user = models.OneToOneField(User)
    key = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.user.username)+str(self.key)


class OrderHistory(models.Model):
    """
    订阅历史
    """
    user = models.OneToOneField(User)
    isbn13 = models.CharField(max_length=200, default=None)
    title = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.TextField()

    def __unicode__(self):
        return str(self.title)