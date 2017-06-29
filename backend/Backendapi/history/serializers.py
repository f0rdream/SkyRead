# coding:utf-8
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    CharField,
    IntegerField,
    Serializer
    )
from .models import SearchHistory
from library.models import BorrowItem
from bookdata.models import Book


class SearchHistorySerializer(ModelSerializer):
    """
    搜索历史序列化器
    """
    user = SerializerMethodField()
    class Meta:
        model = SearchHistory
        fields = [
            'user',
            'key',
        ]
    def get_user(self,obj):
        return obj.user.username


