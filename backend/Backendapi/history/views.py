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
from serializers import (SearchHistorySerializer,
                         BorrowHistorySerializer)
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from models import SearchHistory
from library.models import BorrowItem


class SearchView(APIView):
    """
    搜索历史
    """
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        queryset = SearchHistory.objects.filter(user=user)
        serializer = SearchHistorySerializer(queryset,
                                             data=request.data,
                                             many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class BorrowHistory(APIView):
    """
    借阅历史
    """
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        queryset = BorrowItem.objects.filter(user=user,finish_return=True)
        serializer = BorrowHistorySerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)
