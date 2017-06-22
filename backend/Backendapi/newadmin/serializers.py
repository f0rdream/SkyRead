# coding:utf-8
from django.contrib.auth.models import User
from rest_framework.fields import CharField, BooleanField
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from models import AdminBorrowItemRecord
from library.serializers import BorrowItemDetailSerializer,SuccessOrderItemDetailSerializer
from library.models import PayItem

class UserLoginSerializer(ModelSerializer):
    username = CharField()
    password = CharField(style={'input_type': 'password'})
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }


class BorrowRecordSerializer(ModelSerializer):
    """
    借出操作记录
    """
    item_info = SerializerMethodField()

    class Meta:
        model = AdminBorrowItemRecord
        fields = [
            'record_type',
            'record_time',
            'pay_id',
            'item_info',
        ]

    def get_item_info(self,obj):
        borrow_item = obj.borrow_item
        serializer=BorrowItemDetailSerializer(borrow_item,data={})
        serializer.is_valid(raise_exception=True)
        reply = serializer.data
        reply.pop('borrow_time')
        reply.pop('return_time')
        reply.pop('find_id')
        reply.pop('location')
        return reply


class OrderRecordSerializer(ModelSerializer):
    """
    订阅操作记录
    """
    item_info = SerializerMethodField()
    class Meta:
        model = AdminBorrowItemRecord
        fields = [
            'record_type',
            'record_time',
            'item_info',
        ]
    def get_item_info(self,obj):
        order_item = obj.order_item
        serializer = SuccessOrderItemDetailSerializer(order_item,data={})
        serializer.is_valid(raise_exception=True)
        return serializer.data


