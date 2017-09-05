# coding:utf-8
import time
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
from .models import Comment,Reading,Review
from .serializers import (DoubanCommentSerializer,
                          DoubanReadingSerializer,
                          DoubanReviewSerialzier)
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response


class DoubanCommentListView(APIView):
    """
    豆瓣评论的list View
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,isbn13):
        queryset = Comment.objects.filter(isbn13=isbn13)
        if queryset:
            serializer = DoubanCommentSerializer(queryset,data=request.data,many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        else:
            reply = {}
            reply['error_code'] = 41
            reply['msg'] = 'not found'
            return Response(reply,HTTP_404_NOT_FOUND)


class DoubanCommentDetailView(APIView):
    """
    豆瓣评论的 detail View
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            c = Comment.objects.get(pk=pk)
            serializer = DoubanCommentSerializer(c,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except:
            reply = {}
            reply['error_code'] = 40
            reply['msg'] = 'not found'
            return Response(reply,HTTP_404_NOT_FOUND)


class DoubanReadingListView(APIView):
    """
    豆瓣导读的list view
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,isbn13):
        queryset = Reading.objects.filter(isbn13=isbn13)
        if queryset:
            serializer = DoubanReadingSerializer(queryset, data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        else:
            reply = {}
            reply['error_code'] = 42
            reply['msg'] = 'not found'
            return Response(reply, HTTP_404_NOT_FOUND)


class DoubanReadingDetailView(APIView):
    """
    豆瓣导读的detail view
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            r = Reading.objects.get(pk=pk)
            serializer = DoubanReadingSerializer(r,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except:
            reply = {}
            reply['error_code'] = 43
            reply['msg'] = 'not found'
            return Response(reply,HTTP_404_NOT_FOUND)

class DoubanReviewListView(APIView):
    """
    豆瓣书评list
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, isbn13):
        queryset = Review.objects.filter(isbn13=isbn13)
        if queryset:
            serializer = DoubanReviewSerialzier(queryset, data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        else:
            # 补充书评
            queryset = Review.objects.filter(isbn13=9787205080853)
            serializer = DoubanReviewSerialzier(queryset, data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)


class DoubanReviewDetailView(APIView):
    """
    豆瓣书评detail
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            r = Review.objects.get(pk=pk)
            serializer = DoubanReviewSerialzier(r,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        except:
            reply = {}
            # 加入补充
            reply['error_code'] = 45
            reply['msg'] = 'not found'
            return Response(reply, HTTP_404_NOT_FOUND)


class DoubanReviewLinkDetailView(APIView):
    """
    豆瓣书评link,嵌套的输出
    """
