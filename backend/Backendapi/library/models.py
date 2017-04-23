from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class OrderBar(models.Model):
#     isbn13 = models.CharField(max_length=100,default='')
#     timeline = models.DateTimeField()

class BorrowItem(models.Model):
    isbn13 = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User)
    borrow_time = models.DateTimeField()
    return_time = models.DateTimeField()
    library_name = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=1000,blank=True,null=True)
    qrcode = models.CharField(max_length=1000,blank=True, null=True)
    def get_username(self):
        return self.user.username
class ReturnItem(models.Model):
    isbn13 = models.CharField(max_length=100)
    user = models.ForeignKey(User)