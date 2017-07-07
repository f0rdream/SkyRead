# coding:utf-8
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from serializers import UserLoginSerializer,BorrowRecordSerializer,OrderRecordSerializer
from models import AdminBorrowItemRecord,Sign,SignRecord
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Permission



def get_reply(code,msg):
    reply = dict()
    reply['error_code'] = code
    reply['msg'] = msg
    return reply


@csrf_exempt
@api_view(['GET'])
def is_login_view(request):
    """
    check if the user is login
    :param request:
    :return:
    """
    if request.COOKIES['sessionid']== request.session.session_key:
        return Response({'message':"the user has logged in"}, status=HTTP_200_OK)
    else:
        return Response({'message':"the user is not found"}, status=HTTP_400_BAD_REQUEST)


class AndroidUserLoginAPIView(APIView):
    """
    用户登录
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(get_reply(0,'success'),HTTP_200_OK)
            else:
                return Response(get_reply(120,'fail'),HTTP_403_FORBIDDEN)
        else:
            return Response(get_reply(120, 'fail'), HTTP_403_FORBIDDEN)


class BorrowRecordView(APIView):
    """
    管理员操作的借出记录
    """
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self,request):
        queryset = AdminBorrowItemRecord.objects.filter(user=request.user,
                                                        record_type=1)
        serializer = BorrowRecordSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class ReturnRecordView(APIView):
    """
    管理员操作的归还记录
    """
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request):
        queryset = AdminBorrowItemRecord.objects.filter(user=request.user,
                                                        record_type=2)
        serializer= BorrowRecordSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class OrderRecordView(APIView):
    """
    管理员操作的订阅记录
    """
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self,request):
        queryset = AdminBorrowItemRecord.objects.filter(user=request.user,
                                                        record_type=3)
        serializer = OrderRecordSerializer(queryset,data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class AccountsInfoView(APIView):
    """
    返回管理员信息
    """
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self,request):
        user= request.user
        reply = dict()
        reply['username'] = user.username
        return Response(reply,HTTP_200_OK)


class RecordSumView(APIView):
    """
    记录统计
    """
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self,request):
        user = request.user
        reply = {
            'borrow':len(AdminBorrowItemRecord.objects.filter(user=user,record_type=1)),
            'return':len(AdminBorrowItemRecord.objects.filter(user=user,record_type=2)),
            'order': len(AdminBorrowItemRecord.objects.filter(user=user,record_type=3)),
        }
        return Response(reply,HTTP_200_OK)


class SignItView(APIView):
    """
    员工签到
    """
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self,request):
        user = request.user
        if not user.admin_permission.andriod_permisson:
            return Response(get_reply(130,'not a admin'),HTTP_403_FORBIDDEN)
        else:
            try:
                sign = Sign.objects.get(user=user)
                before_times = sign.times
                before_date = sign.date
                import datetime
                now_date =  datetime.datetime.now().date()
                date_list = str(before_date.date()).split("-")
                year = int(date_list[0])
                month = int(date_list[1])
                day = int(date_list[2])
                before_date = datetime.datetime(year, month, day).date()
                if now_date==before_date:
                    # 今天已经签过
                    return Response(get_reply(131,'have signed'),HTTP_400_BAD_REQUEST)
                else:
                    times = before_times +1
                    sign.delete()
                    new_sign = Sign.objects.create(user=user,times=times)
                    new_sign.save()
                    # 创建当天的签到记录
                    sign_record = SignRecord.objects.create(user=user)
                    sign_record.save()
                    return Response(get_reply(0, 'success'),HTTP_200_OK)
            except Exception as e:
                print e,e.message
                first_sign = Sign.objects.create(user=user,times=1)
                first_sign.save()
                # 创建当天的签到记录
                sign_record = SignRecord.objects.create(user=user)
                sign_record.save()
                return Response(get_reply(0,'success'),HTTP_200_OK)


class InfoView(APIView):
    """
    签到统计
    """
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self,request):
        user = request.user
        username = user.username
        reply = {
            "username": username,
            'borrow': len(AdminBorrowItemRecord.objects.filter(user=user, record_type=1)),
            'return': len(AdminBorrowItemRecord.objects.filter(user=user, record_type=2)),
            'order': len(AdminBorrowItemRecord.objects.filter(user=user, record_type=3)),
        }
        try:
            sign = Sign.objects.get(user=user)
            before_date = sign.date
            import datetime
            now_date = datetime.datetime.now().date()
            date_list = str(before_date.date()).split("-")
            year = int(date_list[0])
            month = int(date_list[1])
            day = int(date_list[2])
            before_date = datetime.datetime(year, month, day).date()
            if now_date == before_date:
                signed = True
            else:
                signed = False
            times = sign.times
            reply['times'] = times
            reply['signed'] = signed
        except:
            reply['times'] = 0
        return Response(reply,HTTP_200_OK)
