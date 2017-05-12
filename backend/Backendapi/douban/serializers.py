from rest_framework.response import Response
from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    CharField,
    IntegerField,
    )

from .models import Comment,Reading,Review
from rest_framework import serializers

class DoubanCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields  =[
            'id',
            'isbn13',
            'author',
            'time',
            'star',
            'vote',
            'content',
        ]


class DoubanReadingSerializer(ModelSerializer):
    class Meta:
        model = Reading
        fields = [
            'id',
            'isbn13',
            'note',
            'content'
        ]


class DoubanReviewSerialzier(ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'isbn13',
            'author',
            'title',
            'content',
        ]
#
# class DoubanReviewLinkSerializer(ModelSerializer):
#     class Meta:
#         model = Review_Link
#         field = [
#             'id',
#             'isbn13',
#             'title',
#             'link',
#         ]