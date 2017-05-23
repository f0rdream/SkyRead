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

# class Refer(models.Model):
#     # create
#     # table
#     # douban_refer(
#     #     isbn13
#     # varchar(200),
#     # refer_id
#     # text)

