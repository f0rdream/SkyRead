# coding:utf-8
import sys

import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view


reload(sys)
sys.setdefaultencoding('utf-8')
import time
from l_lib.function import get_reply
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly
)
from .models import BorrowItem,SuccessOrderItem,WaitOrderItem,PayItem,ReturnItem
from .serializers import (
    BorrowItemCreateSerializer,
    BorrowItemDetailSerializer,
    AddToReturnBarSerializer,
    ReturnBookInfoToAdmin,
    ReturnBookSerializer,
    SuccessOrderItemCreateSerializer,
    SuccessOrderItemDetailSerializer,
    WaitOrderItemCreateSerializer,
    WaitOrderItemDetailSerializer,
    IdListSerializer,
    ISBN13Serializer,
    IdSerializer,
    ReturnItemSerializer,
    BorrowIdListSerializer,
    GetOrderRecordSerializer)

from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from .utils import create_qrcode,create_qrcode_two, get_price, create_order_qrcode,\
    create_return_qrcode
from permissions import have_phone_register
from bookdata.models import Holding,Book
from accounts.models import PhoneUser,WeChatUser
from newadmin.models import AdminBorrowItemRecord

class BorrowItemView(APIView):
    """
    借书item的list和post
    """
    serializer_class = BorrowItemCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    def post(self,request):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        serializer = BorrowItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        isbn13 = serializer.validated_data['isbn13']
        borrow_time = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        return_time = str(time.strftime('%Y-%m-%d',time.localtime(time.time()+2419200)))
        book_id = serializer.validated_data['book_id']
        try:
            holding = Holding.objects.get(id=book_id)
            location = holding.location
            l_loaction = ['总馆', '信息馆', '工学馆', '医学馆']
            guide = ['东', '西', '南', '北']
            location_list = location.split("->")
            location = l_loaction[int(location_list[0])] + "借阅区" + str(location_list[1]) + \
                            "楼" + guide[int(location_list[2])]
            find_id = holding.find_id
        except:
            location = find_id = ''
        user = request.user
        try:
            if BorrowItem.objects.get(user=user,book_id=book_id,in_return_bar=False,
                                      finish_return=False):
                reply = get_reply(10,'item existed')
                return Response(reply,HTTP_200_OK)
        except:
            pass
        # 判断购物车中是否超过2本书籍
        borrow_item_list = BorrowItem.objects.filter(user=user,in_return_bar=False,
                                                     finish_return=False)
        if len(borrow_item_list) >= 2:
            reply = get_reply(11,'item over 2')
            return Response(reply,HTTP_200_OK)

        borrow_item = BorrowItem.objects.create(user=user,
                                                isbn13=isbn13,
                                                borrow_time=borrow_time,
                                                return_time=return_time,
                                                find_id =find_id,
                                                book_id= book_id,
                                                location=location)
        borrow_item.save()
        response = Response(serializer.data,HTTP_201_CREATED)
        return response

    def get(self,request):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        # 判断借书栏中是否超过2本书籍
        queryset = BorrowItem.objects.filter(user=user,in_return_bar=False,finish_return=False)
        serializer = BorrowItemDetailSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data,HTTP_200_OK)
        return response


class BorrowItemDetailDeleteView(APIView):
    """
    借书栏的detail和delete
    """
    permission_classes = [IsAuthenticated]
    content = {}

    def get(self,request,pk):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        try:
            borrow_item = BorrowItem.objects.get(user=user,pk=pk)

            serializer = BorrowItemDetailSerializer(borrow_item,data=request.data)
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.data,HTTP_200_OK)
            return response
        except BorrowItem.DoesNotExist:
            reply = get_reply(12,'item not found')
            response = Response(reply,HTTP_404_NOT_FOUND)
            return response

    def delete(self,request,pk):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        try:
            borrow_item = BorrowItem.objects.get(user=user, pk=pk)
            serializer = BorrowItemDetailSerializer(borrow_item, data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                borrow_item.delete()
                reply = get_reply(0,'success')
                response = Response(reply,HTTP_200_OK)
                return response
            except:
                content = get_reply(13,'delete fail')
                response = Response(content, HTTP_400_BAD_REQUEST)
                return response
        except BorrowItem.DoesNotExist:
            content = get_reply(12,'item not found')
            response = Response(content, HTTP_404_NOT_FOUND)
            return response


class BorrowQrCodeView(APIView):
    """
    生成借书时给管理员扫的二维码(单本书籍)
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        borrow_item = BorrowItem.objects.get(pk=pk)
        ctime = time.time()
        qrtype = "borrow"
        create_qrcode(pk,ctime,qrtype,None)
        url = '/media/borrow_qrcode/'+str(pk)+".png"
        borrow_item.qrcode = url
        borrow_item.save()
        content = {'url':url}
        return Response(content,HTTP_200_OK)


class ManyBorrowQrCodeView(APIView):
    """
    生成借书时给管理员扫的二维码,多本书籍,这个项目限定了2本
    """
    permission_classes = [IsAuthenticated]
    serializer_class = IdListSerializer

    def post(self,request):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_list = serializer.validated_data['id_list']
        price = get_price(id_list)
        ctime = time.time()
        qrtype = 'borrow'
        borrow_id = ""
        for i in id_list:
            borrow_id += 'b' + str(i)  # 参数最后的样子:id = b1b2b3b56
        # 在这里创建一个pay,得到唯一的pay_id
        pay = PayItem.objects.create(user=request.user,
                                     state=False,
                                     confirm=False,
                                     price = price,
                                     borrow_id=borrow_id,
                                     )
        pay.save()
        pay_id = pay.id
        url = create_qrcode(id_list,ctime,qrtype,pay_id)
        reply = dict()
        reply['url'] = url
        reply['pay_id'] = pay_id
        reply['price'] = pay.price
        return Response(reply,HTTP_200_OK)


class VarifyAddToReturnBarView(APIView):
    """
    将借书栏里的书加入到还书栏,验证部分,验证通过则返回书籍信息
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddToReturnBarSerializer

    def post(self,request):
        user = request.user
        if user.has_perm('library.is_a_book_admin'):
            print request.data
            serializer = AddToReturnBarSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            id_list = serializer.validated_data['id_list']
            ctime  = serializer.validated_data['ctime']
            qrtype = serializer.validated_data['qrtype']
            ctime = float(ctime)
            now_time = time.time()
            if now_time - ctime > 120.00:
                reply = get_reply(18,'over time')
                return Response(reply,HTTP_400_BAD_REQUEST)
            if qrtype != 'borrow':
                reply = get_reply(19,'not a borrow')
                return Response(reply,HTTP_400_BAD_REQUEST)
            queryset = list()
            for id in id_list:
                try:
                    borrow_item = BorrowItem.objects.get(pk=id)
                    queryset.append(borrow_item)
                except:
                    pass
            serializer = ReturnBookInfoToAdmin(queryset,
                                               data=[],
                                               many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        else:
            reply = get_reply(16,'not a admin')
            return Response(reply, HTTP_403_FORBIDDEN)


class AddToReturnBarView(APIView):
    """
    管理员核对无误后把书籍加入还书栏,馆藏信息改变
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowIdListSerializer

    def post(self,request):
        user = request.user
        if user.has_perm('library.is_a_book_admin'):
            print request.data
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            id_list = serializer.validated_data['id_list']
            pay_id = serializer.validated_data['pay_id']
            for id in id_list:
                try:
                    borrow_item1 = BorrowItem.objects.get(pk=id)
                    borrow_item1.in_return_bar = True
                    # 获取book_id
                    book_id = borrow_item1.book_id
                    # 修改馆藏信息
                    holding = Holding.objects.get(id=book_id)
                    holding.state = False
                    holding.back_time = borrow_item1.return_time
                    holding.save()
                    borrow_item1.save()
                    # 记录管理员这次借出操作
                    try:
                        record = AdminBorrowItemRecord.objects.create(user=user,
                                                                      record_type=1,
                                                                      borrow_item=borrow_item1,
                                                                      pay_id=pay_id)
                        record.save()
                    except:
                        # TODO 异常处理
                        pass
                except:
                    pass
            reply =  get_reply(0,'success')

            return Response(reply,HTTP_200_OK)
        else:
            reply = get_reply(16,'not a admin')
            return Response(reply, HTTP_403_FORBIDDEN)


class ReturnItemView(APIView):
    """
    还书栏的列表
    """
    serializer_class = BorrowItemCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get(self,request):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        queryset = BorrowItem.objects.filter(user=user,in_return_bar=True,finish_return=False)
        serializer = BorrowItemDetailSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        for i in serializer.data:
            # 在返回数据中,增加到期时间
            return_time = i['return_time']
            date_list = return_time.split("-")
            year = int(date_list[0])
            month = int(date_list[1])
            day = int(date_list[2])
            return_date = datetime.datetime(year, month, day)
            now_date = datetime.datetime.now()
            due =  (return_date - now_date).days
            i['due'] = due
            if i < 7:
                i['due_in_7'] = True
                if i < 3:
                    i['due_in_3'] = True
            else:
                i['due_in_7'] = False
                i['due_in_3'] = False
        response = Response(serializer.data,HTTP_200_OK)
        return response


class ReturnItemDetailDeleteView(APIView):
    """
    还书栏的详情
    """
    permission_classes = [IsAuthenticated]
    content = {}
    def get(self,request,pk):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        user = request.user
        try:
            borrow_item = BorrowItem.objects.get(user=user,pk=pk)
            serializer = BorrowItemDetailSerializer(borrow_item,data=request.data)
            serializer.is_valid(raise_exception=True)
            for i in serializer.data:
                # 在返回数据中,增加到期时间
                return_time = i['return_time']
                date_list = return_time.split("-")
                year = int(date_list[0])
                month = int(date_list[1])
                day = int(date_list[2])
                return_date = datetime.datetime(year, month, day)
                now_date = datetime.datetime.now()
                due = (return_date - now_date).days
                i['due'] = due
                if i < 7:
                    i['due_in_7'] = True
                    if i < 3:
                        i['due_in_3'] = True
                else:
                    i['due_in_7'] = False
                    i['due_in_3'] = False
            response = Response(serializer.data,HTTP_200_OK)
            return response
        except BorrowItem.DoesNotExist:
            reply = get_reply(20,'item not found')
            response = Response(reply,HTTP_404_NOT_FOUND)
            return response


class ManyReturnQrCodeView(APIView):
    """
    难写的生成还书时给管理员扫的二维码,批量还书
    """
    permission_classes = [IsAuthenticated]
    serializer_class  = IdListSerializer

    def post(self,request):
        if not have_phone_register(user=request.user):
            reply = get_reply(17,'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_list = serializer.validated_data['id_list']
        ctime = time.time()
        qrtype = 'return'
        # 创建一个还书item,得到return_id
        return_item = ReturnItem.objects.create(user=request.user,
                                             confirm=False)
        return_item.save()
        return_id = return_item.id
        url = create_return_qrcode(id_list,ctime,qrtype,return_id)
        reply = dict()
        reply['url'] = url
        reply['return_id'] = return_id
        return Response(reply,HTTP_200_OK)


class VarifyReturnBookBarView(APIView):
    """
    准备还书,核对信息部分
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReturnBookSerializer
    def post(self,request):
        user = request.user
        # 此处判断是否是管理员
        if user.has_perm('library.is_a_book_admin'):
            serializer = ReturnBookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            id_list = serializer.validated_data['id_list']
            ctime = serializer.validated_data['ctime']
            qrtype = serializer.validated_data['qrtype']
            ctime = float(ctime)
            now_time = time.time()
            if now_time - ctime > 120.00:
                reply = get_reply(21,'over time')
                return Response(reply, HTTP_400_BAD_REQUEST)
            if qrtype != 'return':
                reply = get_reply(22, 'not a return')
                return Response(reply, HTTP_400_BAD_REQUEST)
            queryset = list()
            for id in id_list:
                try:
                    borrow_item = BorrowItem.objects.get(pk=id)
                    queryset.append(borrow_item)
                except:
                    pass
            serializer = ReturnBookInfoToAdmin(queryset,
                                               data=[],
                                               many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)

            # serializer = ReturnBookSerializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # # 返回书籍信息
            # id = serializer.validated_data['id']
            # borrow_item = BorrowItem.objects.get(pk=id)
             # serializer = ReturnBookInfoToAdmin(borrow_item,data=request.data)
            # serializer.is_valid(raise_exception=True)
            # return Response(serializer.data,HTTP_200_OK)
        else:
            reply = get_reply(23, 'not a admin')
            return Response(reply, HTTP_403_FORBIDDEN)


class FinishReturnView(APIView):
    """
    管理员核对无误后完成还书,更改馆藏信息,退还押金,记录操作
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReturnItemSerializer

    def post(self,request):
        user = request.user
        if user.has_perm('library.is_a_book_admin'):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            id_list = serializer.validated_data['id_list']

            for id in id_list:
                try:
                    borrow_item1 = BorrowItem.objects.get(pk=id)
                    borrow_item1.finish_return = True
                    # 更改还书时间
                    borrow_item1.return_time = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
                    # 获取book_id
                    book_id = borrow_item1.book_id
                    # 修改馆藏信息
                    holding = Holding.objects.get(id=book_id)
                    holding.state = True
                    holding.back_time = "--"
                    holding.save()
                    borrow_item1.save()
                    # 记录归还操作
                    record = AdminBorrowItemRecord.objects.create(user=user,
                                                                  record_type=2,
                                                                  borrow_item=borrow_item1,
                                                                  )
                    record.save()
                except:
                    pass
            # 将还书项的状态变为完成
            return_id = serializer.validated_data['return_id']
            try:
                return_item = ReturnItem.objects.get(id=return_id)
                return_item.confirm = True
                return_user = return_item.user
                # 返还金额
                price = get_price(id_list)
                phone_user = PhoneUser.objects.get(user=return_user)
                phone_user.money += price
                phone_user.save()
                return_item.save()
            except:
                pass
            reply = get_reply(0, 'success')
            return Response(reply,HTTP_200_OK)
        else:
            reply = get_reply(23, 'not a admin')
            return Response(reply, HTTP_403_FORBIDDEN)
        # user = request.user
        # if user.has_perm('library.is_a_book_admin'):
        #     try:
        #         borrow_item = BorrowItem.objects.get(pk=pk)
        #         borrow_item.finish_return = True
        #         borrow_item.save()
        #         return Response({'msg':'Finish returned successful'},HTTP_200_OK)
        #     except:
        #         return Response({'error','Return Item not found'},HTTP_404_NOT_FOUND)
        # else:
        #     reply = {'error': 'you are not a admin'}
        #     return Response(reply, HTTP_403_FORBIDDEN)


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
        book_id = serializer.validated_data['book_id']
        try:
            holding=Holding.objects.get(id=book_id)
            title = holding.book.title
        except:
            title = ''
        # try:
        s = SuccessOrderItem.objects.create(user=user,
                                            isbn13=isbn13,
                                            order_time=order_time,
                                            book_id=book_id,
                                            title=title)
        qrcode = create_order_qrcode(book_id,user.id,title,s.id)
        s.qrcode= qrcode
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
        book_id = serializer.validated_data['book_id']
        try:
            holding = Holding.objects.get(id=book_id)
            title = holding.book.title
            may_return_time = holding.back_time
        except:
            title = ''
            may_return_time = ''
        try:
            s = WaitOrderItem.objects.create(user=user,
                                            isbn13=isbn13,
                                            book_id=book_id,
                                            title=title,
                                            may_return_time=may_return_time)
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


class CurlListView(APIView):
    """
    测试curl
    """
    permission_classes = [AllowAny]
    serializer_class = IdListSerializer

    def post(self,request):
        serializer = IdListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reply = dict()
        reply['id1'] = serializer.data['id_list'][0]
        reply['id2'] = serializer.data['id_list'][1]
        return Response(reply,HTTP_200_OK)


def qrcode_info(request):
    """
    二维码验证,验证时间和管理员
    :param request:
    :return:
    """
    user = request.user
    if user  and  user.has_perm('library.is_a_book_admin'):
        ctime = request.GET.get("ctime")
        id = request.GET.get("id")
        qrtype = request.GET.get('qrtype')
        pay_id = request.GET.get('pay_id')
        return_id = request.GET.get('return_id')
        if not ctime:
            ctime = ""
        if not qrtype:
            qrtype = ""
        if not pay_id:
            pay_id = ''
        if not id:
            id = ""
        if not return_id:
            return_id = ''
        reply = "ctime="+ctime+"&id="+id+"&qrtype="+qrtype+\
                "&pay_id="+pay_id+"&return_id="+return_id
        return HttpResponse(reply)
    else:
        return HttpResponse("您不是SkyRead的管理员,无权操作")


class PayView(APIView):
    permission_classes =  [IsAuthenticated]
    def get(self,request,pay_id):
        try:
            pay = PayItem.objects.get(id=pay_id)
            state = pay.state
            reply = {
                'pay_id':pay_id,
                'state':state
            }
            return Response(reply)
        except:
            reply = get_reply(93,'not found')
            return Response(reply)


class PayItView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pay_id):
        user = request.user
        try:
            pay = PayItem.objects.get(id=pay_id,user=user)
            price = pay.price
            try:
                phone_user = PhoneUser.objects.get(user=user)
                phone_user.money -= price
                if phone_user.money < 0:
                    return Response(get_reply(111,'money not enough'))
                phone_user.save()
            except:
                reply = get_reply(94, 'not found')
                return Response(reply, HTTP_404_NOT_FOUND)
            pay.state = True
            pay.save()
            reply = get_reply(0,'success')
            return Response(reply,HTTP_200_OK)
        except:
            reply = get_reply(94,'not found')
            return Response(reply,HTTP_404_NOT_FOUND)


class AdminConfirmInfo(APIView):
    """
    查看管理员是否已经确认
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pay_id):
        user = request.user
        try:
            pay = PayItem.objects.get(id=pay_id,user=user)
            confirm = pay.confirm
            reply = {
                "pay_id":pay_id,
                "confirm":confirm
            }
            return Response(reply,HTTP_200_OK)
        except:
            reply = get_reply(95, 'not found')
            return Response(reply, HTTP_404_NOT_FOUND)


class ConfirmIt(APIView):
    """
    管理员确认信息接口
    """
    permission_classes = [IsAuthenticated]
    def get(self,request,pay_id):
        try:
            pay = PayItem.objects.get(id=pay_id)
            pay.confirm = True
            pay.save()
            reply = get_reply(0,'success')
            return Response(reply,HTTP_200_OK)
        except:
            reply = get_reply(96,'not found')
            return Response(reply,HTTP_404_NOT_FOUND)


class MyReadedBook(APIView):
    """
    借阅历史
    """
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        try:
            queryset = BorrowItem.objects.filter(finish_return=True)
            serializer = BorrowItemDetailSerializer(queryset,data=request.data,many=True)
            serializer.is_valid(raise_exception=True)
            reply = serializer.data
            return Response(reply,HTTP_200_OK)
        except:
            reply = get_reply(97,'not found')
            return Response(reply,HTTP_404_NOT_FOUND)


class ChangeWaitToSuccess(APIView):
    """
    將等待狀態的书籍约定时间去取
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ISBN13Serializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        wait_id = serializer.validated_data['wait_id']
        order_time = serializer.validated_data['order_time']
        # 删除原来的wait item
        try:
            wait_item = WaitOrderItem.objects.get(id=wait_id)
            wait_item.delete()
            book_id = wait_item.book_id
            isbn13 = " "
            try:
                holding = Holding.objects.get(id=book_id)
                title = holding.book.title
                isbn13 = holding.isbn13
            except:
                title = ''
            # try:
            s = SuccessOrderItem.objects.create(user=request.user,
                                                isbn13=isbn13,
                                                order_time=order_time,
                                                book_id=book_id,
                                                title=title)
            s.save()
            return Response(get_reply(0,'success'),HTTP_200_OK)
        except Exception as e:
            print e
            return Response(get_reply(110,'fail'))


class ContinueReturnBook(APIView):
    """
    正在借阅的书籍自动续借28天,没有到期限内的7天不让借阅
    """
    permission_classes = [IsAuthenticated]
    serializer_class = IdSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data['id']
        try:
            return_book = BorrowItem.objects.get(id=id)
            return_time = return_book.return_time
            date_list = return_time.split("-")
            year = int(date_list[0])
            month = int(date_list[1])
            day = int(date_list[2])
            return_date = datetime.datetime(year, month, day)
            new_return_date = return_date + datetime.timedelta(days=28)
            return_book.return_time = str(new_return_date.date())
            return_book.save()
            return Response(get_reply(0,'success'),HTTP_200_OK)
        except Exception as e:
            print e
            return Response(get_reply(112,'fail'))


class ReturnItemConfirmInfo(APIView):
    """
    获取还书项的信息
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, return_id):
        user = request.user
        try:
            return_item = ReturnItem.objects.get(id=return_id, user=user)
            confirm = return_item.confirm
            reply = {
                "return_id": return_id,
                "confirm": confirm
            }
            return Response(reply, HTTP_200_OK)
        except:
            reply = get_reply(114, 'not found')
            return Response(reply, HTTP_404_NOT_FOUND)


def order_info(request):
    """
    二维码验证,验证时间和管理员
    :param request:
    :return:
    """
    user = request.user
    if user  and  user.has_perm('library.is_a_book_admin'):
        qrtype = request.GET.get("qrtype")
        book_id = request.GET.get("book_id")
        user_id = request.GET.get("id")
        title = request.GET.get('title')
        order_id = request.GET.get('order_id')
        if not book_id:
            book_id = ""
        if not user_id:
            user_id = ""
        if not title:
            title = ''
        if not qrtype:
            qrtype = ''
        nickname=  '获取昵称失败'
        if user_id:
            user = User.objects.get(id=user_id)
            try:
                wechat_user = WeChatUser.objects.get(openid=user.username)
                nickname = wechat_user.nickname
            except:
                nickname = '获取昵称失败'
        reply = "title="+title+"&nickname="+nickname+\
                "&book_id="+book_id+"&qrtype="+qrtype+"&order_id="+order_id
        return HttpResponse(reply)
    else:
        return HttpResponse("您不是SkyRead的管理员,无权操作")


class FinishGiveOrderItemView(APIView):
    """
    完成订阅,返回,记录订阅操作
    """
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = GetOrderRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data['order_id']
        order_item = OrderSuccessItem.objects.get(id=order_id)
        user = request.user
        record = AdminBorrowItemRecord.objects.create(user=user,
                                                      record_type=3,
                                                    order_item=order_item)
        record.save()
        return Response(get_reply(0,'success'))






