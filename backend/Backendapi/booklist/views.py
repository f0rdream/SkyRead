# coding:utf-8
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


class TagBookListView(APIView):
    """
    根据tag检索书籍
    """
    permission_classes = [AllowAny]

    def get(self,request,page):
        import time
        begin =time.time()
        key = self.request.GET.get("key")
        cursor = connection.cursor()
        select_sql ="select isbn13 from bookinfo.isbn13_tag \
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


class RecommandView(APIView):
    """
    得到推荐列表
    """
    permission_classes = [IsAuthenticated]
    # 得到搜索历史,借书栏所有,订阅栏所有,收藏,读书计划,

    def get(self,request):
        user = request.user
        import time
        begin = time.time()
        browsed_book = BrowsedBook.objects.filter(user=user)
        borrow_item = BorrowItem.objects.filter(user=user)
        order_item = BrowsedBook.objects.filter(user=user)
        star_book = StarBook.objects.filter(user=user)
        read_plan = ReadPlan.objects.filter(user=user)
        print time.time()-begin # 0.001
        return Response(get_reply(0,'success'),HTTP_200_OK)



