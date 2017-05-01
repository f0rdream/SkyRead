from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class OrderBar(models.Model):
#     isbn13 = models.CharField(max_length=100,default='')
#     timeline = models.DateTimeField()

class BorrowItem(models.Model):
    isbn13 = models.CharField(max_length=100,default='')
    user = models.ForeignKey(User)
    borrow_time = models.DateTimeField(blank=True,null=True)
    return_time = models.DateTimeField(blank=True,null=True)
    library_name = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=1000,blank=True,null=True)
    qrcode = models.CharField(max_length=1000,blank=True, null=True)
    in_return_bar = models.BooleanField(default=False)
    finish_return = models.BooleanField(default=False)
    def get_username(self):
        return self.user.username
    class Meta:
        permissions =(
            ('is_a_admin','can add book to bar'),
        )