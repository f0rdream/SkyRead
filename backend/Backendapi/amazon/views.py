# Create your views here.
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
from .models import AmazonComment,AmazonInfo
from .serializers import (AmazonCommentSerializer,AmazonInfoSerializer)
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,isbn13):
        queryset = AmazonComment.objects.filter(isbn13=isbn13)
        if queryset:
            serializer = AmazonCommentSerializer(queryset,data=request.data,many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        else:
            reply = {}
            reply['error_code'] = 50
            reply['msg'] = 'not found'
            return Response(reply, HTTP_404_NOT_FOUND)

class InfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,isbn13):
        queryset = AmazonInfo.objects.filter(isbn13=isbn13)
        if queryset:
            serializer = AmazonInfoSerializer(queryset,data=request.data,many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        else:
            reply = {}
            reply['error_code'] = 51
            reply['msg'] = 'not found'
            return Response(reply, HTTP_404_NOT_FOUND)
