# coding:utf-8
from django.contrib.auth.models import User
from rest_framework.fields import CharField, BooleanField
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from newadmin.models import Picture


class PictureSerializer(ModelSerializer):
    picture = SerializerMethodField()

    class Meta:
        model = Picture
        fields = [
            'title',
            'isbn13',
            'picture',
        ]

    def get_picture(self,obj):
        return obj.picture.url
