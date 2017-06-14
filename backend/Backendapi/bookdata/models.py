# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
class Book(models.Model):
    isbn13 = models.CharField(max_length=100,primary_key=True)
    numraters = models.CharField(max_length=100,default='')
    average = models.CharField(max_length=100,default='')
    subtitle =models.CharField(max_length=500,default='')
    author = models.CharField(max_length=1000,default='')
    pubdate = models.CharField(max_length=100,default='')
    origin_title = models.CharField(max_length=500,default='')
    img_id = models.CharField(max_length=100,default='')
    bingding = models.CharField(max_length=100,default='')
    tags = models.TextField(default='')
    catalog = models.TextField(default='')
    pages = models.CharField(max_length=100,default='')
    d_id = models.CharField(max_length=100,default='')
    publisher = models.CharField(max_length=500,default='')
    title = models.CharField(max_length=500,default='')
    summary = models.TextField(default='')
    author_intro = models.TextField(default='')
    price = models.CharField(max_length=100,default='')
    def __unicode__(self):
        return self.title

class Refer(models.Model):
    """
    相关书籍
    """
    isbn13 = models.CharField(max_length=100, primary_key=True)
    refer_id = models.TextField(default=None)
    def __unicode__(self):
        return self.isbn13


class Holding(models.Model):
    """
    馆藏信息
    """
    book = models.ForeignKey(Book)
    isbn13 = models.CharField(max_length=100)
    state = models.BooleanField(default=True)  # 是否在架上
    back_time = models.CharField(max_length=300,default=None)  # 应还日期
    location = models.CharField(max_length=300)
    find_id = models.CharField(max_length=300)
    order_number = models.IntegerField(default=0)
    def __unicode__(self):
        return self.book.title


class StarBook(models.Model):
    """
    我的收藏
    """
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)