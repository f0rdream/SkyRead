# coding:utf-8
import MySQLdb

from django.contrib.auth.models import User
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
from bookdata.models import Book, StarBook
from bookdata.serializers import ShortInto
from library.models import BorrowItem
from models import UserRecommendList, UserPosition
from .serializers import PositionPostSerializer


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
            recommend_list = ['1013129', '2022979', '3426869', '1059419', '1050339',
                             '1085860', '1007914', '1019568', '26340138', '1089243',
                             '1065970', '3598313', '4714734', '1827374', '2159042',
                             '1029159', '6388661', '1030052', '3369600', '1949338',
                             '25747921', '2062200', '1255625', '3646172', '1049219',
                             '1975797', '4074636', '1432596', '2250587', '1045818',
                             '1029791', '1049189', '1948901', '1361264', '10594787',
                             '1013129', '2022979', '3426869', '1059419', '1050339',
                             '1085860', '1007914', '1019568', '26340138', '1089243',
                             '1065970', '3598313', '4714734', '1827374', '2159042',
                             '1029159', '6388661', '1030052', '3369600', '1949338',]
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


class PositionView(APIView):
    """
    每次用户登录的时候通过这个接口提交坐标
    """
    permission_classes = [AllowAny]
    serializer_class = PositionPostSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        x_point = serializer.validated_data['x_point']
        y_point = serializer.validated_data['y_point']
        try:
            user_position = UserPosition.objects.get(user = request.user)
            user_position.x_point = x_point
            user_position.y_point = y_point
            user_position.save()
            return Response(HTTP_200_OK)
        except:
            user_position = UserPosition.objects.create(user=request.user,
                                                        x_point = x_point,
                                                        y_point = y_point)
            user_position.save()
            return Response(HTTP_200_OK)


class NearByBookView(APIView):
    """
    附近的书接口
    算出x,y相差小于1的,把借书栏和收藏栏的书籍推出来
    """
    permission_classes = [AllowAny]

    def get(self,request):
        user = request.user
        try:
            user_position = UserPosition.objects.get(user=user)
            user_x_point = user_position.x_point
            user_y_point = user_position.y_point
            all_users = User.objects.all()
            nearby_users = list()
            # 找到附近的用户
            for u in all_users:
                if u.id == user.id:
                    continue
                try:
                    u_position = UserPosition.objects.get(user=u)
                    u_x_point = user_position.x_point
                    u_y_point = u_position.y_point
                    if abs(user_x_point-u_x_point) < 1 and abs(user_y_point-u_y_point) < 1:
                        nearby_users.append(u)
                except:
                    continue
            # 找到附近的用户之后,从他们的书单中抽取书籍
            nearby_books_isbn13 = list()
            for near_user in nearby_users:
                try:
                    nearby_borrow_items = BorrowItem.objects.filter(user=near_user)
                    for item in nearby_borrow_items:
                        nearby_books_isbn13.append(item.isbn13)
                except Exception as e:
                    pass
                try:
                    nearby_star_books = StarBook.objects.filter(user=near_user)
                    for s in nearby_star_books:
                        nearby_books_isbn13.append(s.book.isbn13)
                except:
                    pass
            # 返回书籍信息
            queryset = list()
            for isbn13 in nearby_books_isbn13:
                try:
                    book = Book.objects.get(isbn13=isbn13)
                    queryset.append(book)
                except:
                    pass
            serializer = ShortInto(queryset[:20], many=True, data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        except Exception as e:
            print e
            reply = get_reply(153, "can't find position")
            return Response(reply, HTTP_404_NOT_FOUND)





