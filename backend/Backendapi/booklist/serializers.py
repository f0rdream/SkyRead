import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from accounts.models import WeChatUser
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    CharField,
    IntegerField,
    Serializer
    )
from rest_framework import serializers
from .models import UserPosition


class IsbnSerializer(serializers.Serializer):
    isbn13 = CharField(max_length=200)


class PositionPostSerializer(ModelSerializer):
    class Meta:
        model = UserPosition
        fields = [
            'x_point',
            'y_point'
        ]



