# coding:utf-8
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
from .models import (Book, Refer, Holding,
                     StarBook, Comment,
                     ReadPlan, ImageFile,
                     Note, PlanRecord)


class BookInfoSerializer(ModelSerializer):
    """
    基本信息序列化器
    因为爬取数据的时候空数据为('',),所以需要处理
    author_intro暂时没有处理
    """
    isbn13 = SerializerMethodField()
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
                if author == '' or author == '[美国]' or author == '[美]' \
                        or author == '[日]' or author == '[奥地利]' or author == '[瑞典]'\
                        or author == '[英]':
                    continue
                else:
                    if len(author) > 15:
                        author = author[:15]
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
    图书信息的简短信息
    """
    isbn13 = SerializerMethodField()
    author = SerializerMethodField()
    img_id = SerializerMethodField()
    publisher = SerializerMethodField()
    class Meta:
        model = Book
        fields = [
            'isbn13',
            'title',
            'author',
            'img_id',
            'publisher',
            'average',
            'price',
        ]

    def get_isbn13(self,obj):
        return obj.isbn13

    def get_img_id(self,obj):
        img_id = obj.img_id
        if img_id == "update_image":
            return None
        else:
            return img_id

    def get_publisher(self,obj):
        publisher = obj.publisher
        if publisher == "('',)":
            return None
        else:
            return publisher

    def get_author(self,obj):
        authors = obj.author
        if authors == '' or authors == '&':
            return None
        else:
            author_list = []
            authors = authors.split('&')
            for author in authors:
                # 处理作者,美国,美
                if author == '' or author == '[美国]' or author == '[美]' \
                        or author == '[日]' or author == '[奥地利]' or author == '[瑞典]' \
                        or author == '[英]':
                    continue
                else:
                    if len(author) > 15:
                        author = author[:15]
                    author_list.append(author)
            return author_list


class SearchSerializer(Serializer):
    key = CharField()


class HoldingSerializer(ModelSerializer):
    """
    馆藏信息序列化器
    """
    state = SerializerMethodField()
    location = SerializerMethodField()
    class Meta:
        model = Holding
        fields = [
            'id',
            'isbn13',
            'state',
            'back_time',
            'location',
            'find_id',
            'order_number',
        ]
    def get_state(self,obj):
        state = obj.state
        if state == 1:
            real_state = '在架上'
        else:
            real_state = '已经借出'
        return real_state
    def get_location(self,obj):
        location = obj.location
        l_loaction = ['总馆', '信息馆', '工学馆', '医学馆']
        guide = ['东', '西', '南', '北']
        location_list = location.split("->")
        real_location = l_loaction[int(location_list[0])]+"借阅区"+str(location_list[1])+\
                        "楼"+guide[int(location_list[2])]
        return real_location


class StarBookSerializer(Serializer):
    """
    创建我的收藏
    """
    isbn13 = CharField()


class StarBookDetailSerializer(ModelSerializer):
    """
    我的收藏序列化
    """
    id = SerializerMethodField()
    short_info = SerializerMethodField()

    class Meta:
        model = StarBook
        fields = [
            'id',
            'short_info',
        ]

    def get_id(self,obj):
        id = obj.id
        return id

    def get_short_info(self,obj):
        book = obj.book
        short_info = ShortInto(book,data={})
        short_info.is_valid(raise_exception=True)
        return short_info.data


class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


class CommentDetailSerializer(ModelSerializer):
    nickname = SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['content','nickname']
    def get_nickname(self,obj):
        username = obj.user.username
        try:
            wechat_user = WeChatUser.objects.get(openid=username)
            nickname = wechat_user.nickname
            return nickname
        except:
            return '--'


class PostReadPlanSerializer(ModelSerializer):
    class Meta:
        model= ReadPlan
        fields = [
            'isbn13',
            'begin_time',
            'end_time',
        ]

    def validate(self, data):
        isbn13 = data.get('isbn13')
        begin_time = data.get('begin_time')
        end_time = data.get('end_time')

        if not isbn13:
            raise ValidationError('lack isbn13')
        if not begin_time:
            raise ValidationError('lack begin_time')
        if not end_time:
            raise ValidationError('lack end_time')
        return data


class ReadPlanDetailSerializer(ModelSerializer):
    title = SerializerMethodField()
    isbn13 = SerializerMethodField()
    author = SerializerMethodField()
    img_id = SerializerMethodField()

    class Meta:
        model = ReadPlan
        fields = [
            'id',
            'title',
            'isbn13',
            'begin_time',
            'end_time',
            'sum_page',
            'now_page',
            'last_date',
            'author',
            'img_id',
        ]

    def get_isbn13(self,obj):
        return obj.isbn13

    def get_title(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            title = book.title
            return title
        except:
            return "--"

    def get_author(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            authors = book.author
            if authors == '' or authors == '&':
                return None
            else:
                author_list = []
                authors = authors.split('&')
                for author in authors:
                    if author == '':
                        continue
                    else:
                        if len(author) > 15:
                            author = author[:15]
                        author_list.append(author)
                return author_list
        except:
            return "--"

    def get_img_id(self,obj):
        isbn13 = obj.isbn13
        try:
            book = Book.objects.get(isbn13=isbn13)
            img_id = book.img_id
            if img_id == "update_image":
                return None
            else:
                return img_id
        except:
            return "--"


class Img2TextSerializer(ModelSerializer):
    class Meta:
        model = ImageFile
        fields = [
            'image'
        ]


class NotePostSerializer(ModelSerializer):
    """
    创建新的笔记
    """
    class Meta:
        model = Note
        fields = [
            'content',
            'isbn13',
            'comment',
        ]


class NoteGetSerializer(ModelSerializer):
    """
    查看已有的笔记
    """
    title = SerializerMethodField()
    content = SerializerMethodField()
    isbn13 = SerializerMethodField()
    date = SerializerMethodField()
    comment = SerializerMethodField()
    book_img_url = SerializerMethodField()
    shared = SerializerMethodField()

    class Meta:
        model = Note
        exclude = ['user']

    def get_title(self,obj):
        return obj.title

    def get_content(self,obj):
        return obj.content

    def get_isbn13(self,obj):
        return obj.isbn13

    def get_date(self,obj):
        return obj.date

    def get_comment(self,obj):
        return obj.comment

    def get_book_img_url(self,obj):
        return obj.book_img_url

    def get_shared(self,obj):
        return obj.shared


class RecordPostSerializer(ModelSerializer):
    class Meta:
        model = PlanRecord
        fields = [
            'now_page'
        ]


class RecordGetSerializer(ModelSerializer):
    plan_for = SerializerMethodField()

    class Meta:
        model = PlanRecord
        fields = "__all__"
    def get_plan_for(self,obj):
        return obj.plan_for.id
