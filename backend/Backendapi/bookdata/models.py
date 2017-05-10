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
class BookReview(models.Model):
    """
    豆瓣书评
    """
    review_id = models.CharField(max_length=100, primary_key=True)
    isbn13 = models.CharField(max_length=100)
    author = models.CharField(max_length=1000,blank=True,null=True)
    title = models.CharField(max_length=1000,blank=True,null=True)
    content = models.TextField(max_length=1000,blank=True,null=True)
    is_link = models.BooleanField(default=False)

class BookComment(models.Model):
    """
    豆瓣评论
    """
    isbn13 = models.CharField(max_length=100)
    author = models.CharField(max_length=1000, blank=True, null=True)
    time = models.CharField(max_length=200, blank=True, null=True)
    star = models.CharField(max_length=200, blank=True, null=True)
    vote = models.CharField(max_length=200, blank=True, null=True)
    content = models.IntegerField(default=0)


