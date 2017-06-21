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