# coding:utf-8
import time

from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly
)
from .models import Book,Refer
from .serializers import (BookInfoSerializer,
                          ShortInto,SearchSerializer)
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
        except Exception as e:
            print e
            reply = get_reply(91,e)
            return Response(reply,HTTP_404_NOT_FOUND)

