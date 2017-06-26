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
    # 豆瓣TOP100书单
    douban_top_100_list=['1770782', '1084336', '1008145', '1082154', '25862578',
                         '3259440', '1046265', '3211779', '2567698', '1017143',
                         '1007305', '1016300', '1040771', '20427187', '6082808',
                         '5275059', '1461903', '1200840', '1141406', '1041007',
                         '10554308', '3066477', '1068920', '4238362', '5363767',
                         '4242172', '1083428', '1090043', '1026425', '2256039',
                         '1873231', '1071241', '3995526', '1400705', '1039487',
                         '1041482', '1059406', '1023045', '2209098', '4742918',
                         '1022060', '4886245', '3879301', '1529893', '1009257',
                         '1057244', '1858513', '1066462', '4913064', '1082334',
                         '25747921', '2062200', '1255625', '3646172', '1049219',
                         '1975797', '4074636', '1432596', '2250587', '1045818',
                         '1029791', '1049189', '1948901', '1361264', '10594787',
                         '1013129', '2022979', '3426869', '1059419', '1050339',
                         '1085860', '1007914', '1019568', '26340138', '1089243',
                         '1065970', '3598313', '4714734', '1827374', '2159042',
                         '1029159', '6388661', '1030052', '3369600', '1949338',
                         '5317075',]
    def get(self,request):
        user = request.user
        import time
        begin = time.time()
        browsed_book = BrowsedBook.objects.filter(user=user)
        borrow_item = BorrowItem.objects.filter(user=user)
        order_item = BrowsedBook.objects.filter(user=user)
        star_book = StarBook.objects.filter(user=user)
        read_plan = ReadPlan.objects.filter(user=user)
        sys_user_isbn13 = list()
        for book in browsed_book:
            isbn13 = book.isbn13
            sys_user_isbn13.append(isbn13)
        for book in borrow_item:
            isbn13 = book.isbn13
            sys_user_isbn13.append(isbn13)
        for star_book in star_book:
            isbn13 = star_book.book.isbn13
            sys_user_isbn13.append(isbn13)
        for book in read_plan:
            isbn13 = book.isbn13
            sys_user_isbn13.append(isbn13)
        # get book_d_id:
        sys_user_douban_id = list()
        for isbn13 in sys_user_isbn13:
            sql = "select d_id from bookdata_book where isbn13='%s' " %isbn13
            cursor = connection.cursor()
            cursor.execute(sql)
            douban_id_rs = cursor.fetchall()
            for row in douban_id_rs:
                douban_id = row[0]
                sys_user_douban_id.append(douban_id)

        print time.time()-begin # 0.001
        return Response(get_reply(0,'success'),HTTP_200_OK)



