from django.db import models
# coding:utf-8
# 测试isbn13:9787111013853

class Comment(models.Model):
    """
    评论模型
    """
    isbn13 = models.CharField(max_length=200,default=None)
    author = models.CharField(max_length=200,null=True,blank=True,default=None)
    time = models.CharField(max_length=200,null=True,blank=True,default=None)
    star = models.IntegerField(default=None)
    vote = models.CharField(max_length=200,null=True,blank=True,default=None)
    content = models.TextField(default=None)
    def __unicode__(self):
        return self.isbn13

class Reading(models.Model):
    """
    导读模型
    """
    isbn13 = models.CharField(max_length=200,default=None)
    title = models.TextField(default=None)
    note = models.TextField(default=None)
    def __unicode__(self):
        return self.title
class Review(models.Model):
    """
    书评模型
    """
    isbn13 = models.CharField(max_length=200, default=None)
    title = models.TextField(default=None)
    author = models.TextField(default=None)
    content = models.TextField(default=None)
    def __unicode__(self):
        return self.title
# class Review_Link(models.Model):
#     """
#     书评link模型
#     """
#     isbn13 =  models.CharField(max_length=200, default=None)
#     title = models.TextField(default=None)
#     link = models.TextField(default=None)