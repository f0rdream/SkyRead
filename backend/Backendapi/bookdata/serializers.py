# coding:utf-8
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    CharField,
    IntegerField,
    )
from .models import Book


class BookInfoSerializer(ModelSerializer):
    """
    基本信息序列化器
    因为爬取数据的时候空数据为('',),所以需要处理
    author_intro暂时没有处理
    """
    isbn13 =  SerializerMethodField()
    numraters = SerializerMethodField()
    subtitle = SerializerMethodField()
    author = SerializerMethodField()
    pubdate = SerializerMethodField()
    origin_title = SerializerMethodField()
    img_id = SerializerMethodField()
    bingding = SerializerMethodField()
    tags = SerializerMethodField()
    pages =  SerializerMethodField()
    publisher = SerializerMethodField()
    summary =  SerializerMethodField()
    catalog = SerializerMethodField()
    class Meta:
        model = Book
        fields = [
            'isbn13',
            'title',
            'subtitle',
            'origin_title',
            'author',
            'author_intro',
            'summary',
            'average',
            'numraters',
            'pubdate',
            'publisher',
            'img_id',
            'pages',
            'tags',
            'bingding',
            'price',
            'd_id',
            'catalog',
        ]

    def get_numraters(self,obj):
        numraters = obj.numraters
        if numraters == "('',)":
            return None
        else:
            return numraters

    def get_subtitle(self,obj):
        subtitle = obj.subtitle
        if subtitle == "('',)":
            return None
        else:
            return subtitle

    def get_author(self,obj):
        authors = obj.author
        if authors == '' or authors == '&':
            return None
        else:
            author_list = []
            authors = authors.split('&')
            for author in authors:
                if author == '':
                    continue
                else:
                    author_list.append(author)
            return author_list

    def get_pubdate(self,obj):
        pubdate = obj.pubdate
        if pubdate == "('',)":
            return None
        else:
            return pubdate

    def get_origin_title(self,obj):
        origin_title = obj.origin_title
        if origin_title == "('',)":
            return None
        else:
            return origin_title

    def get_img_id(self,obj):
        img_id = obj.img_id
        if img_id == "update_image":
            return None
        else:
            return img_id

    def get_bingding(self,obj):
        bingding = obj.bingding
        if bingding == "('',)":
            return None
        else:
            return bingding

    def get_tags(self,obj):
        tags = obj.tags
        if tags == '':
            return None
        else:
            taglist = []
            tags = tags.split('&')
            for tag in tags:
                if tag == '':
                    continue
                else:
                    taglist.append(tag)
            return taglist

    def get_pages(self,obj):
        pages = obj.pages
        if pages == "('',)":
            return None
        else:
            return pages

    def get_publisher(self,obj):
        publisher = obj.publisher
        if publisher == "('',)":
            return None
        else:
            return publisher

    def get_summary(self,obj):
        summary = obj.summary
        if summary == "('',)":
            return None
        else:
            return summary

    def get_isbn13(self,obj):
        return obj.isbn13
    def get_catalog(self,obj):
        catalog = obj.catalog
        if catalog == "('',)":
            return None
        else:
            return catalog.replace('(收起)','')


class ShortInto(ModelSerializer):
    """
    图书信息的简短
    """
