# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BorrowItem(models.Model):
    isbn13 = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User)
    borrow_time = models.CharField(max_length=200,default=None,blank=True,null=False)
    return_time = models.CharField(max_length=200,default=None,blank=True,null=False)
    book_id = models.TextField(default=None,blank=False,null=False)
    find_id = models.TextField(default=None,blank=False,null=False)
    location = models.CharField(max_length=1000,blank=True,null=True)
    qrcode = models.CharField(max_length=1000,blank=True, null=True)
    in_return_bar = models.BooleanField(default=False)
    finish_return = models.BooleanField(default=False)
    def get_username(self):
        return self.user.username
    def __unicode__(self):
        return self.user.username+"find_id="+str(self.book_id)

    class Meta:
        permissions =(
            ('is_a_book_admin','can add book to bar'),
        )


class SuccessOrderItem(models.Model):
    isbn13 = models.CharField(max_length=100, default='')
    title = models.TextField(default=None)
    user = models.ForeignKey(User)
    order_time = models.DateTimeField(blank=False,null=False,default=None)
    book_id = models.IntegerField(default=0)
    qrcode = models.CharField(max_length=1000, blank=True, null=True)


class WaitOrderItem(models.Model):
    isbn13 = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User)
    title = models.TextField(default=None)
    book_id = models.IntegerField(default=0)
    may_return_time = models.CharField(max_length=200,default=None)
    return_state = models.BooleanField(default=False)


class PayItem(models.Model):
    """
    支付
    """
    user = models.ForeignKey(User)
    state = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    confirm = models.BooleanField(default=False)  # 管理员是否确认

    def __unicode__(self):
        return str(self.id)


class ReturnItem(models.Model):
    """
    用于还书确认
    """
    user = models.ForeignKey(User)
    confirm = models.BooleanField(default=False)  # 管理员是否确认

    def __unicode__(self):
        return str(self.id)


