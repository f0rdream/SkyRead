# coding:utf-8
import time
from django.shortcuts import render
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly
)
from .models import BorrowItem,SuccessOrderItem,WaitOrderItem
from .serializers import (
    BorrowItemCreateSerializer,
    BorrowItemDetailSerializer,
    AddToReturnBarSerializer,
    ReturnBookInfoToAdmin,
    ReturnBookSerializer,
    SuccessOrderItemCreateSerializer,
    SuccessOrderItemDetailSerializer,
    WaitOrderItemCreateSerializer,
    WaitOrderItemDetailSerializer)
from .utils import create_qrcode
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils import depwd
# Create your views here.


class BorrowItemView(APIView):
    """
    借书item的list和post
    """
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
        borrowItem.save()
        response = Response(serializer.data,HTTP_201_CREATED)
        return response
    def get(self,request):
        user = request.user
        queryset = BorrowItem.objects.filter(user=user,in_return_bar=False,finish_return=False)
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
            if borrow_item.in_return_bar == True:
                reply = {'error':'This book is in your return bar now'}
                return Response(reply,HTTP_404_NOT_FOUND)
            if borrow_item.finish_return == True:
                reply = {'error':'This book has finished returned now'}
                return Response(reply,HTTP_404_NOT_FOUND)
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
            if borrow_item.in_return_bar == True:
                reply = {'error':'This book is in your return bar now'}
                return Response(reply,HTTP_404_NOT_FOUND)
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


class BorrowQrCodeView(APIView):
    """
    生成借书时给管理员扫的二维码
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        borrow_item = BorrowItem.objects.get(pk=pk)
        isbn13 = borrow_item.isbn13
        isbn13 = isbn13
        ctime = time.time()
        qrtype = "borrow"
        create_qrcode(pk,ctime,qrtype)
        url = '/media/borrow_qrcode/'+str(pk)+".png"
        borrow_item.qrcode = url
        borrow_item.save()
        content = {'url':url}
        return Response(content,HTTP_200_OK)


class VarifyAddToReturnBarView(APIView):
    """
    将借书栏里的书加入到还书栏,验证部分
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddToReturnBarSerializer
    def post(self,request):
        user = request.user
        # 此处判断是否是管理员
        if user.has_perm('library.is_a_admin'):
            serializer = AddToReturnBarSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            id = serializer.validated_data['id']
            borrow_item = BorrowItem.objects.get(pk=id)
            serializer = ReturnBookInfoToAdmin(borrow_item,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        else:
            reply = {'error': 'you are not a admin'}
            return Response(reply, HTTP_403_FORBIDDEN)


class AddToReturnBarView(APIView):
    """
    管理员核对无误后把书籍加入还书栏
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        user = request.user
        if user.has_perm('library.is_a_admin'):
            try:
                borrow_item = BorrowItem.objects.get(pk=pk)
                borrow_item.in_return_bar = True
                borrow_item.save()
                return Response({'msg':'Add to return bar successful'},HTTP_200_OK)
            except:
                return Response({'error','Borrow Item not found'},HTTP_404_NOT_FOUND)
        else:
            reply = {'error': 'you are not a admin'}
            return Response(reply, HTTP_403_FORBIDDEN)


class ReturnItemView(APIView):
    serializer_class = BorrowItemCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    def get(self,request):
        user = request.user
        queryset = BorrowItem.objects.filter(user=user,in_return_bar=True,finish_return=False)
        serializer = BorrowItemDetailSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data,HTTP_200_OK)
        return response


class ReturnItemDetailDeleteView(APIView):
    """

    """
    permission_classes = [IsAuthenticated]
    content = {}
    def get(self,request,pk):
        user = request.user
        try:
            borrow_item = BorrowItem.objects.get(user=user,pk=pk)
            if borrow_item.in_return_bar == False:
                reply = {'error':'This book is in your borrow bar now'}
                return Response(reply,HTTP_404_NOT_FOUND)
            if borrow_item.finish_return == True:
                reply = {'error':'This book has finished returned now'}
                return Response(reply,HTTP_404_NOT_FOUND)
            serializer = BorrowItemDetailSerializer(borrow_item,data=request.data)
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.data,HTTP_200_OK)
            return response
        except BorrowItem.DoesNotExist:
            content = {'error':"Can't find the item or you don't have this item"}
            response = Response(content,HTTP_404_NOT_FOUND)
            return response


class ReturnQrCodeView(APIView):
    """
    生成还书时给管理员扫的二维码
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        borrow_item = BorrowItem.objects.get(pk=pk)
        isbn13 = borrow_item.isbn13
        isbn13 = isbn13
        ctime = time.time()
        qrcode = "return"
        create_qrcode(pk,ctime,qrcode)
        url = '/media/return_qrcode/'+str(pk)+".png"
        borrow_item.qrcode = url
        borrow_item.save()
        content = {'url':url}
        return Response(content,HTTP_200_OK)


class VarifyReturnBookBarView(APIView):
    """
    准备还书,核对信息部分
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReturnBookSerializer
    def post(self,request):
        user = request.user
        # 此处判断是否是管理员
        if user.has_perm('library.is_a_admin'):
            serializer = ReturnBookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # 返回书籍信息
            id = serializer.validated_data['id']
            borrow_item = BorrowItem.objects.get(pk=id)
            serializer = ReturnBookInfoToAdmin(borrow_item,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        else:
            reply = {'error': 'you are not a admin'}
            return Response(reply, HTTP_403_FORBIDDEN)


class FinishReturnView(APIView):
    """
    管理员核对无误后完成借书
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        user = request.user
        if user.has_perm('library.is_a_admin'):
            try:
                borrow_item = BorrowItem.objects.get(pk=pk)
                borrow_item.finish_return = True
                borrow_item.save()
                return Response({'msg':'Finish returned successful'},HTTP_200_OK)
            except:
                return Response({'error','Return Item not found'},HTTP_404_NOT_FOUND)
        else:
            reply = {'error': 'you are not a admin'}
            return Response(reply, HTTP_403_FORBIDDEN)


class OrderSuccessView(APIView):
    """
    这本书有藏书,那么就可以访问这个接口，加入订阅栏，状态为预约成功
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SuccessOrderItemCreateSerializer

    def post(self,request):
        user= request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        isbn13 = serializer.validated_data['isbn13']
        order_time = serializer.validated_data['order_time']
        location = serializer.validated_data['location']
        find_id  = serializer.validated_data['find_id']
        if_phone = serializer.validated_data['if_phone']
        # try:
        s = SuccessOrderItem.objects.create(user=user,isbn13=isbn13,order_time=order_time,
                                            location=location,find_id=find_id,if_phone=if_phone)
        s.save()
        return Response(serializer.data,HTTP_201_CREATED)
        # except Exception as e:
        #     print e.message
        #     reply = {}
        #     reply['error_code'] = 20
        #     reply['msg'] = 'fail'
        #     return Response(reply,HTTP_400_BAD_REQUEST)

    def get(self,request):
        """
        返回成功状态的订阅栏的详情
        :param request:
        :return:
        """
        user = request.user
        queryset = SuccessOrderItem.objects.filter(user=user)
        serializer = SuccessOrderItemDetailSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class SuccessOrderDetailView(APIView):
    """
    返回或删除单个订阅成功的详情
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            s = SuccessOrderItem.objects.get(pk=pk)
            serializer = SuccessOrderItemDetailSerializer(s,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except:
            reply = {}
            reply['error_code'] = 22
            reply['msg'] = 'not found'
            return Response(reply,HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        try:
            s = SuccessOrderItem.objects.get(pk=pk)
            s.delete()
            reply = {'msg':'success'}
            return Response(reply,HTTP_200_OK)
        except:
            reply = {}
            reply['error_code'] = 23
            reply['msg'] = 'fail'
            return Response(reply,HTTP_400_BAD_REQUEST)


class OrderWaitView(APIView):
    """
    如果没有藏书,则加入订阅栏，状态为等待
    """
    permission_classes = [IsAuthenticated]
    serializer_class = WaitOrderItemCreateSerializer

    def post(self, request):
        user=request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        isbn13 = serializer.validated_data['isbn13']
        location = serializer.validated_data['location']
        find_id = serializer.validated_data['find_id']
        if_phone = serializer.validated_data['if_phone']
        try:
            s = WaitOrderItem.objects.create(user=user,
                                             isbn13=isbn13,
                                            location=location,
                                            find_id=find_id,
                                            if_phone=if_phone)
            s.save()
            return Response(serializer.data, HTTP_201_CREATED)
        except:
            reply = {}
            reply['error_code'] = 21
            reply['msg'] = 'fail'

    def get(self, request):
        """
        返回等待状态的订阅栏的详情
        :param request:
        :return:
        """
        user = request.user
        queryset = WaitOrderItem.objects.filter(user=user)
        serializer = WaitOrderItemDetailSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, HTTP_200_OK)


class WaitOrderDetailView(APIView):
    """
    返回或删除单个订阅等待的详情
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            w = WaitOrderItem.objects.get(pk=pk)
            print w
            serializer = WaitOrderItemDetailSerializer(w,data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except:
            reply = {}
            reply['error_code'] = 24
            reply['msg'] = 'not found'
            return Response(reply,HTTP_404_NOT_FOUND)
    def delete(self,request,pk):
        try:
            w = WaitOrderItem.objects.get(pk=pk)
            w.delete()
            reply = {'msg':'success'}
            return Response(reply,HTTP_200_OK)
        except:
            reply = {}
            reply['error_code'] = 23
            reply['msg'] = 'fail'
            return Response(reply,HTTP_400_BAD_REQUEST)




