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
from .models import BorrowItem
from .serializers import (
    BorrowItemCreateSerializer,
    BorrowItemDetailSerializer,)

from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,)
from rest_framework.response import Response
# Create your views here.
class BorrowItemView(APIView):
    serializer_class = BorrowItemCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    def post(self,request):
        serializer = BorrowItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        isbn13 = serializer.validated_data['isbn13']
        borrow_time = serializer.validated_data['borrow_time']
        return_time = serializer.validated_data['return_time']
        library_name = serializer.validated_data['library_name']
        location = serializer.validated_data['location']
        user = request.user
        content = {}
        # if user.borrow > 2 then error
        # if user.borrow_set.
        try:
            if BorrowItem.objects.get(user=user,isbn13=isbn13):
                content = {'error':'The book you want to borrow is existing!'}
                response = Response(content,HTTP_400_BAD_REQUEST)
                return response
        except:
            pass
        borrowItem =BorrowItem.objects.create(user=user,isbn13=isbn13,borrow_time=borrow_time,
                                  return_time=return_time,library_name=library_name,location=location)
        response = Response(serializer.data,HTTP_201_CREATED)
        return response
    def get(self,request):
        user = request.user
        queryset = BorrowItem.objects.filter(user=user)
        serializer = BorrowItemDetailSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data,HTTP_200_OK)
        return response
    # def delete(self,request):
    #     user = request.user
    #     serial
    #     try:
    #         item = BorrowItem.objects.get()

    # def delete(self,request):
class BorrowItemDetailDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    content = {}
    def get(self,request,pk):
        user = request.user
        try:
            borrow_item = BorrowItem.objects.get(user=user,pk=pk)
            serializer = BorrowItemDetailSerializer(borrow_item,data=request.data)
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.data,HTTP_200_OK)
            return response
        except BorrowItem.DoesNotExist:
            content = {'error':"Can't find the item or you don't have this item"}
            response = Response(content,HTTP_404_NOT_FOUND)
            return response
    def delete(self,request,pk):
        user = request.user
        try:
            borrow_item = BorrowItem.objects.get(user=user, pk=pk)
            serializer = BorrowItemDetailSerializer(borrow_item, data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                borrow_item.delete()
                content = {'Msg':'Delete successful'}
                response = Response(content,HTTP_200_OK)
                return response
            except:
                content = {'error':'Delete failed'}
                response = Response(content, HTTP_400_BAD_REQUEST)
                return response
            # response = Response(serializer.data, HTTP_200_OK)
            # return response
        except BorrowItem.DoesNotExist:
            content = {'error': "Can't find the item or you don't have this item"}
            response = Response(content, HTTP_404_NOT_FOUND)
            return response

