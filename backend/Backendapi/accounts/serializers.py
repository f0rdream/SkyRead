# coding:utf-8
from django.contrib.auth.models import User

from .models import WeChatUser,PhoneUser
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    CharField,
    IntegerField,
    )

from .a_lib.vlidators import CheckString,PhoneValid
>>>>>>> fa6dd802a9733da1692cdc1ed1cd74d2e3c7bca6
from rest_framework import serializers


class UserProfileDetailSerializer(ModelSerializer):
    """
    用户基本信息序列化器
    """
    have_phone =  SerializerMethodField()
    phone_number = SerializerMethodField()
    email = SerializerMethodField()
    real_name = SerializerMethodField()
    class Meta:
        model = WeChatUser
        fields = [
            'nickname',
            'headimgurl',
            'openid',
            'sex',
            'phone_number',
            'email',
            'real_name',
            'have_phone',
        ]

    def get_phone_number(self,obj):
        username = obj.openid
        u = User.objects.get(username=username)
        try:
            p = PhoneUser.objects.get(user=u)
            return p.phone_number
        except:
            return None

    def get_email(self,obj):
        username = obj.openid
        u = User.objects.get(username=username)
        try:
            p = PhoneUser.objects.get(user=u)
            return p.email
        except:
            return None

    def get_real_name(self,obj):
        username = obj.openid
        u = User.objects.get(username=username)
        try:
            p = PhoneUser.objects.get(user=u)
            return p.real_name
        except:
            return None

    def get_have_phone(self,obj):
        username = obj.openid
        u = User.objects.get(username=username)
        try:
            p = PhoneUser.objects.get(user=u)
            return 1
        except:
            return 0



class PhoneUserCreateSerializer(ModelSerializer):
    """
    用户手机绑定序列化器
    """
    captcha = CharField(allow_null=False)

    class Meta:
        model = PhoneUser
        fields = [
            'phone_number',
            'email',
            'real_name',
            'captcha'
        ]
    def validate(self, data):
        phone_number = data.get('phone_number')
        captcha = data.get('captcha')
        if not phone_number:
            raise ValidationError('lack phone_number')
        if not captcha:
            raise ValidationError('lack captcha')
        return data


class CheckAPISerializer(serializers.Serializer):
    """
    用户信息查重 API 序列化器
    """
    phone_number = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    def validate(self, data):
        phone_number = data.get('phone_number')
        if not phone_number:
            serializers.ValidationError('lack phone number')
        return data


class SendMessageSerializer(serializers.Serializer):
    """
    发送验证码序列化器,暂时只提供注册
    """
    phone_number = serializers.CharField()
    def validate(self, data):
        phone_number = data.get('phone_number')
        if not phone_number:
            serializers.ValidationError('lack phone number')
        return data
