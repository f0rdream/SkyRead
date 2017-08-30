# coding:utf-8
from django.db import models
from django.contrib.auth.models import User


class GuideBookManager(models.Manager):
    def get_guide_book(self,id):
        return super(GuideBookManager,
                     self).get_queryset().filter(book_guide=id).order_by('-average')


class Book(models.Model):
    objects = models.Manager()  # 默认的管理器
    guide_objects = GuideBookManager() # 用于图书导航的管理器
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
    book_guide = models.IntegerField(default=0)
    title_for_index = models.TextField(default=None,null=False)
    author_for_index = models.TextField(default=None, null=False)

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


class Comment(models.Model):
    """
    书籍评论
    """
    user = models.ForeignKey(User)
    isbn13 = models.CharField(max_length=100)
    content = models.TextField(default=None)


class ReadPlan(models.Model):
    """
    读书计划
    """
    user = models.ForeignKey(User)
    isbn13 = models.CharField(max_length=100)
    begin_time = models.DateTimeField(max_length=100, default=None)
    end_time = models.DateTimeField(max_length=100, default=None)
    sum_page = models.IntegerField(default=0)
    now_page = models.IntegerField(default=0)
    last_date = models.CharField(default=u'xxxx-xx-xx', max_length=200)


class BrowsedBook(models.Model):
    """
    用户浏览过的书籍
    """
    user = models.ForeignKey(User)
    isbn13 = models.CharField(max_length=200)


class Note(models.Model):
    """
    笔记
    """
    user = models.ForeignKey(User)
    content = models.TextField()
    comment = models.TextField(default="comment")
    title = models.CharField(max_length=1000)
    book_img_url = models.CharField(max_length=1000,default="img_url")
    isbn13 = models.CharField(max_length=1000, default=u"-1")
    date = models.CharField(max_length=200)


class ImageFile(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to = './img2text/')

    def __unicode__(self):
        return self.image.url


class PlanRecord(models.Model):
    """
    打卡记录
    """
    plan_for = models.ForeignKey(ReadPlan)
    last_page = models.IntegerField(default=0)
    record_date = models.CharField(max_length=200, default=u"xxxx-xx-xx")
    now_page = models.IntegerField(default=0)


