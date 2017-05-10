from rest_framework.response import Response
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    CharField,
    IntegerField,
    )

from .models import AmazonComment,AmazonInfo
from rest_framework import serializers

class AmazonCommentSerializer(ModelSerializer):
    class Meta:
        model = AmazonComment
        fields = [
            'id',
            'isbn13',
            'author',
            'content',
        ]

class AmazonInfoSerializer(ModelSerializer):
    class Meta:
        model = AmazonInfo
        fields =[
            'id',
            'isbn13',
            'title',
            'average',
            'erecommand',
            'frecommand',
            'mrecommand',
        ]