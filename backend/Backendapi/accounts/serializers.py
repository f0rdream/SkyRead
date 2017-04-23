# coding:utf-8
from rest_framework.serializers import SerializerMethodField,ModelSerializer
from .models import WeChatUser
class UserProfileDetailSerializer(ModelSerializer):
    class Meta:
        model = WeChatUser
        fields = [
            'nickname',
            'openid',
            'sex',
            'province',
            'city',
            'country',
            'headimgurl'
        ]





















