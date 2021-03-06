# coding:utf-8
from django.contrib.auth.models import User

from .models import WeChatUser, PhoneUser, FeedBack, StarList, BookListComment
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    CharField,
    IntegerField,
    )
from bookdata.models import NoteComment

from .accounts_lib.vlidators import CheckString,PhoneValid
from rest_framework import serializers


class FeedBackDetailSerializer(ModelSerializer):
    """
    用户反馈详情的序列化器
    """
    class Meta:
        model = FeedBack
        fields = '__all__'


class FeedBackSerializer(ModelSerializer):
    """
    用户反馈序列化器
    """
    class Meta:
        model = FeedBack
        fields = [
            'content'
        ]


class UserProfileDetailSerializer(ModelSerializer):
    """
    用户基本信息序列化器
    """
    have_phone = SerializerMethodField()
    phone_number = SerializerMethodField()
    email = SerializerMethodField()
    real_name = SerializerMethodField()
    message_info = SerializerMethodField()
    money = SerializerMethodField()
    recommend_times = SerializerMethodField()
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
            'money',
            'message_info',
            'recommend_times',
        ]

    def get_message_info(self,obj):
        username = obj.openid
        try:
            user =User.objects.get(username=username)
            phone_user = PhoneUser.objects.get(user=user)
            reply = dict()
            order_message = phone_user.order_message
            return_message = phone_user.return_message
            reply['order_msg'] = order_message
            reply['return_msg'] = return_message
            return reply
        except:
            return None


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
    def get_money(self,obj):
        openid = obj.openid
        try:
            user =User.objects.get(username=openid)
            phone_user = PhoneUser.objects.get(user=user)
            money = phone_user.money
            return money
        except:
            return -1

    def get_recommend_times(self,obj):
        openid = obj.openid
        try:
            user =User.objects.get(username=openid)
            phone_user = PhoneUser.objects.get(user=user)
            money = phone_user.recommend_times
            return money
        except:
            return None


class PhoneUserCreateSerializer(ModelSerializer):
    """
    用户手机绑定序列化器
    """
    captcha = CharField(allow_null=False)

    class Meta:
        model = PhoneUser
        fields = [
            'phone_number',
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


class ChangeTimesSerializer(serializers.Serializer):
    """
    更改推荐频率
    """
    recommend_times = serializers.IntegerField()

    def validate(self, data):
        recommend_times = data.get('recommend_times')
        if not recommend_times:
            serializers.ValidationError('lack recommend_times')
        return data


class AddLabelSerializer(serializers.Serializer):
    """
    添加标签到首页
    """
    label_name = serializers.CharField(max_length=1000)


class LabelSerializer(ModelSerializer):
    """
    查看自己添加的首页分类：标签
    """
    class Meta:
        model = StarList
        exclude = ['user_list_id', 'user', 'list_type']


class BookListCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=1000)
    comment = serializers.CharField(max_length=10000)
    isbn13_list = serializers.ListField(child=IntegerField())


class BookListIdSerializer(serializers.Serializer):
    list_id = serializers.CharField(max_length=200)


class CycleCommnetSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000)


class ListCommentDetailSerializer(ModelSerializer):
    nickname = SerializerMethodField()
    class Meta:
        model = BookListComment
        fields = [
            'nickname',
            'content',
        ]

    def get_nickname(self, obj):
        username = obj.user.username
        try:
            wechat_user = WeChatUser.objects.get(openid=username)
            nickname = wechat_user.nickname
            return nickname
        except:
            return '--'


class NoteCommentDetailSerializer(ModelSerializer):
    nickname = SerializerMethodField()
    class Meta:
        model = NoteComment
        fields = [
            'nickname',
            'content',
        ]

    def get_nickname(self, obj):
        username = obj.user.username
        try:
            wechat_user = WeChatUser.objects.get(openid=username)
            nickname = wechat_user.nickname
            return nickname
        except:
            return '--'





