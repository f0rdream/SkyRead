# coding:utf-8
import time
from rest_framework.response import Response
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    ListField,
    CharField,
    IntegerField,
    )

from accounts.models import WeChatUser
from rest_framework import serializers
from .models import BorrowItem,WaitOrderItem,SuccessOrderItem
from bookdata.models import Book
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bookdata.models import Holding

class BorrowItemCreateSerializer(ModelSerializer):
    class Meta:
        # borrow_time = DateTimeField(allow_null=False)
        # return_time = DateTimeField(allow_null=False)
        model=BorrowItem
        fields =[
            'isbn13',
            'book_id',
        ]

    def validate(self, data):
        isbn13 = data.get('isbn13')
        book_id = data.get('book_id')
        if not isbn13:
            raise ValidationError('lack isbn13')
        if not book_id:
            raise ValidationError('lack book_id')
        return data


class BorrowItemDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    nickname = SerializerMethodField()
    borrow_time = SerializerMethodField()
    return_time = SerializerMethodField()
    title = SerializerMethodField()
    price = SerializerMethodField()
    class Meta:
        model = BorrowItem
        fields = [
            'id',
            'isbn13',
            'user',
            'borrow_time',
            'return_time',
            'book_id',
            'find_id',
            'location',
            'nickname',
            'title',
            'price',
        ]

    def get_user(self,obj):
        return str(obj.user.username)

    def get_nickname(self,obj):
        username = obj.user.username
        try:
            wechatuser = WeChatUser.objects.get(openid=username)
            nickname = wechatuser.nickname
            return nickname
        except:
            return None

    def get_borrow_time(self,obj):
        return obj.borrow_time

    def get_return_time(self,obj):
        return obj.return_time

    def get_title(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            title = book.title
            return title
        except:
            return None

    def get_price(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            price = book.price
            return price
        # 这里通过BookModel 拿到价格
        except:
            return None
# class QrCodeSerializer(ModelSerializer):
#     class


class AddToReturnBarSerializer(serializers.Serializer):
    """
    验证部分
    """
    id_list = ListField(
        child = IntegerField()
    )
    ctime = CharField()
    qrtype = CharField()
    def validate(self, data):
        id_list = data.get('id_list')
        ctime = data.get('ctime')
        qrtype = data.get('qrtype')
        if not id_list:
            raise ValidationError('lack id_list')
        if not ctime:
            raise ValidationError('lack ctime')
        if not qrtype:
            raise ValidationError('lack type')
        return data

    # def get_isbn13(self,vali):


class ReturnBookSerializer(serializers.Serializer):
    id_list = ListField(
        child=IntegerField()
    )
    ctime = CharField()
    qrtype = CharField()
    def validate(self, data):
        id_list = data.get('id_list')
        ctime = data.get('ctime')
        qrtype = data.get('qrtype')
        if not id_list:
            raise ValidationError('lack id_list')
        if not ctime:
            raise ValidationError('lack ctime')
        if not qrtype:
            raise ValidationError('lack type')

        return data


class ReturnBookInfoToAdmin(ModelSerializer):
    title =  SerializerMethodField()
    price = SerializerMethodField()
    nickname =  SerializerMethodField()
    image = SerializerMethodField()

    class Meta:
        model = BorrowItem
        fields=[
            'id',
            'nickname',
            'isbn13',
            'title',
            'image',
            'price',
            'borrow_time',
            'return_time',
            'book_id',
            'find_id',
            'location',
        ]

    def get_image(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            title = book.img_id
            return title
        except:
            return None

    def get_title(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            title = book.title
            return title
        except:
            return None

    def get_price(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            price = book.price
            return price
        # 这里通过BookModel 拿到价格
        except:
            return None

    def get_nickname(self,obj):
        username = obj.user.username
        try:
            wechatuser = WeChatUser.objects.get(openid=username)
            nickname = wechatuser.nickname
            return nickname
        except:
            return None


class SuccessOrderItemCreateSerializer(ModelSerializer):
    """
    订阅栏中预订成功的创建序列化器
    """
    class Meta:
        model = SuccessOrderItem
        fields = [
            'isbn13',
            'order_time',
            'book_id'
        ]

    def validate(self, data):
        isbn13 = data.get('isbn13')
        order_time = data.get('order_time')
        book_id = data.get('book_id')

        if not isbn13:
            raise ValidationError('lack isbn13')
        if not order_time:
            raise ValidationError('lack order_time')
        if not book_id:
            raise ValidationError('lack book_id')
        return data


class WaitOrderItemCreateSerializer(ModelSerializer):
    """
    订阅栏中等待状态的创建序列化器
    """
    class Meta:
        model = WaitOrderItem
        fields = [
            'isbn13',
            'book_id'
        ]

    def validate(self, data):
        isbn13 = data.get('isbn13')
        book_id = data.get('book_id')
        if not isbn13:
            raise ValidationError('lack isbn13')
        if not book_id:
            raise ValidationError('lack book_id')

        return data


class SuccessOrderItemDetailSerializer(ModelSerializer):
    """
    订阅栏中成功状态的详情的序列化器
    """
    id = SerializerMethodField()
    order_time = SerializerMethodField()
    class Meta:
        model = SuccessOrderItem
        fields= [
            'id',
            'isbn13',
            'book_id',
            'title',
            'order_time',
            'qrcode',
        ]

    def get_order_time(self,obj):
        return obj.order_time
    def get_id(self,obj):
        return obj.pk


class WaitOrderItemDetailSerializer(ModelSerializer):
    """
    订阅栏中等待状态的详情的序列化器
    """
    id = SerializerMethodField()
    return_state = SerializerMethodField()

    class Meta:
        model = WaitOrderItem
        fields= [
            'id',
            'isbn13',
            'title',
            'book_id',
            'may_return_time',
            'return_state',
        ]

    def get_id(self,obj):
        return obj.pk

    def get_return_state(self,obj):
        book_id = obj.book_id
        try:
            holding = Holding.objects.get(id=book_id)
            return_state = holding.state
            return return_state
        except:
            return False

class IdListSerializer(serializers.Serializer):
    """
    批量生成的id的list
    """
    id_list = ListField(
        child = IntegerField()
    )


class BorrowIdListSerializer(serializers.Serializer):
    """
    批量生成的id的list
    """
    id_list = ListField(
        child = IntegerField()
    )
    pay_id = IntegerField()


class ISBN13Serializer(serializers.Serializer):
    """
    ISBN13
    """
    wait_id = serializers.IntegerField()
    order_time = serializers.DateTimeField()


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ReturnItemSerializer(serializers.Serializer):
    """
    批量生成的id的list
    """
    id_list = ListField(
        child = IntegerField()
    )
    return_id = IntegerField()


class GetOrderRecordSerializer(serializers.Serializer):
    """
    生成取书籍记录
    """
    order_id = IntegerField()
