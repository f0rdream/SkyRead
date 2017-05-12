# coding:utf-8
from django.db import models
# Create your models here.


class AmazonComment(models.Model):
    isbn13 = models.CharField(max_length=200, default=None)
    author = models.TextField(default=None)
    content = models.TextField(default=None)

class AmazonInfo(models.Model):
    """
    亚马逊基本信息
    """
    title = models.TextField(default=None)
    isbn13 = models.CharField(max_length=200, default=None)
    average = models.CharField(max_length=200,default=None)
    erecommand = models.TextField(default=None)
    frecommand = models.TextField(default=None)
    mrecommand = models.TextField(default=None)