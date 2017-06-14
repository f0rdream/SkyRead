#coding:utf-8
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class SearchHistory(models.Model):
    """
    搜索历史
    """
    user = models.OneToOneField(User)
    key = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.user.username)+str(self.key)
