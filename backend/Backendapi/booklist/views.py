# coding:utf-8
import MySQLdb

from django.shortcuts import render
from django.db.models import Q
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from library.permissions import have_phone_register
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from l_lib.function import get_reply
from django.db import connection
# Create your views here.
from bookdata.models import BrowsedBook,ReadPlan,StarBook
from bookdata.models import Book
from bookdata.serializers import ShortInto
from library.models import BorrowItem,SuccessOrderItem,WaitOrderItem
from recommend import book_recommend,user_recommend
from django.core.cache import cache
import time
from models import UserRecommendList


class TagBookListView(APIView):
    """
    根据tag检索书籍
    """
    permission_classes = [AllowAny]

    def get(self,request,page):
        import time
        begin = time.time()
        key = self.request.GET.get("key")
        cursor = connection.cursor()
        select_sql = "select isbn13 from bookinfo.isbn13_tag \
        where tag='%s' limit  %d,20" % (key,int(page))
        cursor.execute(select_sql)
        tag_rs = cursor.fetchall()
        queryset = list()
        for row in tag_rs:
            isbn13 = row[0]
            try:
                book = Book.objects.get(isbn13=isbn13)
                queryset.append(book)
            except:
                pass
        serializer = ShortInto(queryset, many=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, HTTP_200_OK)


class AuthorBookListView(APIView):
    """
    根据author检索书籍
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,page):
        import time
        begin =time.time()
        key = self.request.GET.get("key")
        cursor = connection.cursor()
        select_sql ="select isbn13 from bookinfo.isbn13_author where author='%s' \
         order by average desc limit %d,20 " % (key,int(page))
        cursor.execute(select_sql)
        author_rs = cursor.fetchall()
        queryset = list()
        for row in author_rs:
            isbn13 = row[0]
            try:
                book = Book.objects.get(isbn13=isbn13)
                queryset.append(book)
            except:
                pass
        serializer = ShortInto(queryset, many=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        print time.time()-begin
        return Response(serializer.data, HTTP_200_OK)


class RecommendView(APIView):
    """
    得到推荐列表,加入default_dict缓存和用户书单缓存(1天,那么每天深夜更新一次)
    """
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        try:
            recommend_list = UserRecommendList.objects.get(user=user)
            isbn13_list = recommend_list.isbn13_list.split("&")
            queryset = list()
            for isbn13 in isbn13_list[1:]:
                try:
                    book = Book.objects.get(isbn13=isbn13)
                    queryset.append(book)
                except:
                    pass
            serializer = ShortInto(queryset, many=True, data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        except:
            recommend_list = ['1770782', '1084336', '1008145', '1082154', '25862578',
                             '3259440', '1046265', '3211779', '2567698', '1017143',
                             '1007305', '1016300', '1040771', '20427187', '6082808',
                             '5275059', '1461903', '1200840', '1141406', '1041007',
                             '10554308', '3066477', '1068920', '4238362', '5363767',
                             '4242172', '1083428', '1090043', '1026425', '2256039',]
            queryset = list()
            for douban_id in recommend_list:
                isbn13_sql = "select isbn13 from bookdata_book where d_id='%s' " % str(douban_id)
                cursor = connection.cursor()
                cursor.execute(isbn13_sql)
                isbn13_rs = cursor.fetchall()

                for row in isbn13_rs:
                    isbn13 = row[0]
                    try:
                        book = Book.objects.get(isbn13=isbn13)
                        queryset.append(book)
                    except Exception as e:
                        print e
                        pass
            serializer = ShortInto(queryset, many=True, data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)


class SameUserBookList(APIView):
    """
    得到相似用户名单
    """
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        recommend_list = UserRecommendList.objects.get(user=user)
        user_like = recommend_list.user_like
        if user_like:
            user_list = user_like.split("&")
            reply = {
                'user_list':user_list[1:]
            }
            return Response(reply,HTTP_200_OK)
        else:
            reply = {
                'user_list':[]
            }
            return Response(reply,HTTP_200_OK)


class SameUserBookDetail(APIView):
    """
    得到相似用户的书单
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,order):
        order = int(order)
        user = request.user
        recommend_list = UserRecommendList.objects.get(user=user)
        user_like = recommend_list.user_like
        if user_like:
            user_list = user_like.split("&")
            db_username = user_list[order]
            cursor = connection.cursor()
            sql = "select * from user_record.user_item where user='%s'" % db_username
            cursor.execute(sql)
            rs = cursor.fetchall()
            items_list = list()
            for row in rs:
                items_in_string = row[1]
                items_list = items_in_string.split("&")
                items_list.remove("")
            queryset = list()
            for douban_id in items_list:
                isbn13_sql = "select isbn13 from bookdata_book where d_id='%s' " % douban_id
                cursor = connection.cursor()
                cursor.execute(isbn13_sql)
                isbn13_rs = cursor.fetchall()
                for row in isbn13_rs:
                    isbn13 = row[0]
                    try:
                        book = Book.objects.get(isbn13=isbn13)
                        queryset.append(book)
                    except:
                        pass
            serializer = ShortInto(queryset[:20], many=True, data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        else:
            return Response(get_reply(150,'no data'),HTTP_200_OK)



