# coding:utf-8
import time

from django.db.models import Q
from django.http import HttpResponse
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly
)
from .models import Book,Refer,Holding,StarBook
from .serializers import (BookInfoSerializer,
                          ShortInto, SearchSerializer, HoldingSerializer, StarBookSerializer)
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from history.models import SearchHistory
from l_lib.function import get_reply
class BookInfoView(APIView):
    serializer_class = BookInfoSerializer
    permission_classes = [AllowAny]
    # authentication_classes = [SessionAuthentication]
    def get(self,request,isbn13):
        isbn13 = str(isbn13)
        try:
            book = Book.objects.get(isbn13=isbn13)
        except:
            return Response({'error': 'can not find this book'}, HTTP_404_NOT_FOUND)
        serializer = BookInfoSerializer(book,data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, HTTP_200_OK)
        return response


class Serach(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        key = self.request.GET.get("key")
        # 存入搜索历史
        try:
            s = SearchHistory.objects.create(user=request.user,key=key)
            s.save()
        except:
            pass
        if key:
            title_queryset = Book.objects.filter(Q(title__icontains=key) |
                                                 Q(subtitle__icontains=key))
            author_queryset = Book.objects.filter(Q(author__icontains=key))
            title_serializer = ShortInto(title_queryset,data=request.data,many=True)
            title_serializer.is_valid(raise_exception=True)
            author_serializer = ShortInto(author_queryset,data=request.data,many=True)
            author_serializer.is_valid(raise_exception=True)
            reply = dict()
            reply['title_result'] = title_serializer.data
            reply['author_result'] = author_serializer.data
            return Response(reply,HTTP_200_OK)
        else:
            reply = {'msg':'None'}
            return Response(reply,HTTP_200_OK)

class ReferBookView(APIView):
    """
    相关书籍
    """
    permission_classes = [AllowAny]

    def get(self,request,isbn13):
        try:
            r = Refer.objects.get(isbn13=isbn13)
            refer_id = r.refer_id
            refer_object_list = list()
            refer = refer_id.split("&")
            for i in range(1, len(refer)):
                try:
                    b = Book.objects.get(d_id=refer[i])
                    refer_object_list.append(b)
                except:
                    pass
            serializer = ShortInto(refer_object_list, data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except:
            reply = get_reply(91,"not found")
            return Response(reply,HTTP_404_NOT_FOUND)



class HoldingView(APIView):
    """
    馆藏信息VIEW
    """
    permission_classes = [AllowAny]
    def get(self,request,isbn13):
        try:
           queryset = Holding.objects.filter(isbn13=isbn13)
           if not queryset:
               reply = get_reply(92, "not found")
               return Response(reply, HTTP_404_NOT_FOUND)
           serializer = HoldingSerializer(queryset,data=request.data,many=True)
           serializer.is_valid(raise_exception=True)
           return Response(serializer.data,HTTP_200_OK)
        except Exception as e:
            reply = get_reply(92,"not found")
            return Response(reply,HTTP_404_NOT_FOUND)


class StarBookView(APIView):
    """
    我的收藏书籍
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StarBookSerializer
    def post(self,request):
        serializer = StarBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        isbn13 = serializer.validated_data['isbn13']
        try:
            book = Book.objects.get(isbn13=isbn13)
            user = request.user
            # 判断这本书是否已经存在
            try:
                before_book = StarBook.objects.get(user=user,book=book)
                return Response(get_reply(98, 'fail'))
            except:
                pass
            starbook = StarBook.objects.create(user=user,book=book)
            starbook.save()
            return Response(get_reply(0,'success'))
        except:
            return Response(get_reply(98,'fail'))
    def get(self,request):
        user = request.user
        queryset = StarBook.objects.filter(user=user)
        book_list = list()
        for starbook in queryset:
            book = starbook.book
            book_list.append(book)
        serializer = ShortInto(book_list,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class GuideBookView(APIView):
    """
    书籍导航
    """
    permission_classes =  [IsAuthenticated]

    def get(self,request,guide_id,page):
        if page < 1:
            return Response(get_reply(81,'error page'),HTTP_404_NOT_FOUND)
        begin_page = (int(page)-1)*20
        end_page = begin_page+20
        try:
            queryset = Book.guide_objects.get_guide_book(int(guide_id))[begin_page:end_page]
            serializer = ShortInto(queryset,many=True,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except Exception as e:
            return Response(get_reply(0,e),HTTP_404_NOT_FOUND)
