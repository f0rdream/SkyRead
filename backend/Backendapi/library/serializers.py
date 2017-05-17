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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BorrowItemCreateSerializer(ModelSerializer):
    class Meta:
        # borrow_time = DateTimeField(allow_null=False)
        # return_time = DateTimeField(allow_null=False)
        model=BorrowItem
        fields =[
            'isbn13',
            'borrow_time',
            'return_time',
            'borrow_find_id',
            'library_name',
            'location',
        ]

    def validate(self, data):
        isbn13 = data.get('isbn13')
        borrow_time = data.get('borrow_time')
        return_time = data.get('return_time')
        library_name = data.get('library_name')
        location = data.get('location')
        find_id = data.get('borrow_find_id')
        if not isbn13:
            raise ValidationError('lack isbn13')
        if not borrow_time:
            raise ValidationError('lack borrow_time')
        if not return_time:
            raise ValidationError('lack return_time')
        if not library_name:
            raise ValidationError('lack library_name')
        if not location:
            raise ValidationError('lack location')
        if not find_id:
            raise ValidationError('lack find_id')
        return data

class BorrowItemDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    nickname = SerializerMethodField()
    borrow_time = SerializerMethodField()
    return_time = SerializerMethodField()

    class Meta:
        model = BorrowItem
        fields = [
            'id',
            'isbn13',
            'user',
            'borrow_time',
            'return_time',
            'borrow_find_id',
            'library_name',
            'location',
            'nickname',
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
        ctime = float(ctime)
        now_time = time.time()
        if now_time - ctime > 120.00:
            raise ValidationError('This qrcode is overdue')
        try:
            BorrowItem.objects.get(pk=id)
        except:
            raise ValidationError('This borrow item is not exist')
        if qrtype != 'borrow':
            raise ValidationError('this is not a borrow qrcode')
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
        ctime = float(ctime)
        now_time = time.time()
        if now_time - ctime > 120.00:
            raise ValidationError('This qrcode is overdue')
        try:
            BorrowItem.objects.get(pk=id)
        except:
            raise ValidationError('This return item is not exist')
        if qrtype != 'return':
            raise ValidationError('This is not a return qrcode')
        return data


class ReturnBookInfoToAdmin(ModelSerializer):
    title =  SerializerMethodField()
    prices = SerializerMethodField()
    nickname =  SerializerMethodField()
    class Meta:
        model = BorrowItem
        fields=[
            'id',
            'nickname',
            'isbn13',
            'title',
            'prices',
            'borrow_time',
            'return_time',
            'find_id',
            'library_name',
            'location',
        ]

    def get_title(self,obj):
        isbn13 = obj.isbn13
        # 这里通过BookModel 拿到标题
        return "This is a test title"

    def get_prices(self,obj):
        isbn13 = obj.isbn13
        # 这里通过BookModel 拿到价格
        return "This is a test price"

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
            'location',
            'find_id',
            'if_phone',
        ]

    def validate(self, data):
        isbn13 = data.get('isbn13')
        order_time = data.get('order_time')
        location = data.get('location')
        find_id = data.get('find_id')
        if_phone = data.get('if_phone')

        if not isbn13:
            raise ValidationError('lack isbn13')
        if not order_time:
            raise ValidationError('lack order_time')
        if not location:
            raise ValidationError('lack location')
        if not find_id:
            raise ValidationError('lack find_id')
        if not if_phone:
            raise ValidationError('lack if_phone')
        return data


class WaitOrderItemCreateSerializer(ModelSerializer):
    """
    订阅栏中等待状态的创建序列化器
    """
    class Meta:
        model = WaitOrderItem
        fields = [
            'isbn13',
            'location',
            'find_id',
            'if_phone',
        ]
    def validate(self, data):
        isbn13 = data.get('isbn13')
        location = data.get('location')
        find_id = data.get('find_id')
        if_phone = data.get('if_phone')

        if not isbn13:
            raise ValidationError('lack isbn13')
        if not location:
            raise ValidationError('lack location')
        if not find_id:
            raise ValidationError('lack find_id')
        if not if_phone:
            raise ValidationError('lack if_phone')
        return data


class SuccessOrderItemDetailSerializer(ModelSerializer):
    """
    订阅栏中成功状态的详情的序列化器
    """
    id = SerializerMethodField()

    class Meta:
        model = SuccessOrderItem
        fields= [
            'id',
            'isbn13',
            'location',
            'find_id',
            'if_phone',
            'status',
            'order_time',
        ]

    def get_id(self,obj):
        return obj.pk

class WaitOrderItemDetailSerializer(ModelSerializer):
    """
    订阅栏中等待状态的详情的序列化器
    """
    id = SerializerMethodField()

    class Meta:
        model = WaitOrderItem
        fields= [
            'id',
            'isbn13',
            'location',
            'find_id',
            'if_phone',
            'status',
        ]

    def get_id(self,obj):
        return obj.pk


class IdListSerializer(serializers.Serializer):
    """
    批量生成的id的list
    """
    id_list = ListField(
        child = IntegerField()
    )
