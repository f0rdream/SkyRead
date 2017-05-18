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
        fields = [
            'user',
            'key',
            'time'
        ]
    def get_user(self,obj):
        return obj.user.username


class BorrowHistorySerializer(ModelSerializer):
    """
    借阅历史序列化器
    """
    user = SerializerMethodField()
    title = SerializerMethodField()

    class Meta:
        model = BorrowItem
        fields = [
            'user',
            'isbn13',
            'title',
            'borrow_time',
            'return_time',
            'borrow_find_id',
            'library_name',
            'location',
        ]

    def get_user(self,obj):
        return obj.user.username

    def get_title(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            title = book.title
            return title
        except:
            return None