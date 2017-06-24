# coding:utf-8
from django.contrib.auth.models import User
from django.db import models

from library.models import BorrowItem,SuccessOrderItem
from library.models import PayItem
# Create your models here.


class AdminBorrowItemRecord(models.Model):
    """
    管理员操作记录
    """
    user = models.ForeignKey(User)
    record_type = models.IntegerField(default=0)  # 操作类型:借出 归还 处理订阅
    record_time = models.DateTimeField(auto_now_add=True)  # 操作时间
    borrow_item = models.ForeignKey(BorrowItem,blank=True,null=True)
    pay_id = models.IntegerField(default=0)
    order_item = models.ForeignKey(to=SuccessOrderItem,blank=True,null=True)
    about_user =models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.user.username)


class Admin_Permission(models.Model):
    """
    自己写的用户权限限制
    """
    user = models.OneToOneField(User)
    andriod_permisson = models.BooleanField(default=False)
    admin_permisson = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


class Sign(models.Model):
    """
    员工签到
    """
    times = models.IntegerField(default=0)
    user = models.OneToOneField(User)
    date = models.DateTimeField(auto_now_add=True)


class SignRecord(models.Model):
    """
    记录员工签到表
    """
    user= models.ForeignKey(User)
    date  =models.DateTimeField(auto_now_add=True)


class ExcelFile(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    excel = models.FileField(upload_to='./newadmin/upload/')
    def __unicode__(self):
        return self.excel.url


