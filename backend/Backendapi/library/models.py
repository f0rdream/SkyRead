# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BorrowItem(models.Model):
    isbn13 = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User)
    borrow_time = models.DateTimeField(default=None,blank=True,null=False)
    return_time = models.DateTimeField(default=None,blank=True,null=False)
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
    user = models.ForeignKey(User)
    order_time = models.DateTimeField(blank=True,null=True,default=None)
    location = models.CharField(max_length=1000,default=None)
    find_id = models.CharField(max_length=1000,default=None)
    if_phone = models.IntegerField(default=0)
    status = models.IntegerField(default=0)


class WaitOrderItem(models.Model):
    isbn13 = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User)
    location = models.CharField(max_length=1000,default=None)
    find_id = models.CharField(max_length=1000,default=None)
    if_phone = models.IntegerField(default=0)
    status = models.IntegerField(default=1)

class PayItem(models.Model):
    """
    支付
    """
    user = models.ForeignKey(User)
    state = models.BooleanField(default=False)
