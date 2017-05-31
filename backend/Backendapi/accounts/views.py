# coding:utf-8
import requests
from django.shortcuts import render
from serializers import (UserProfileDetailSerializer,
                        SendMessageSerializer,
                        CheckAPISerializer,
                        PhoneUserCreateSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
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
from .models import WeChatUser,PhoneUser
from a_lib.phone_verify import send_message,verify


class UserProfileDetailAPIView(APIView):
    """
    用户基本信息API
    """
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'user_stu_id'
    def get(self,request):
        openid = request.user.username
        w = WeChatUser.objects.get(openid=openid)
        serializer = self.serializer_class(w,data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class CheckAPIView(APIView):
    """
    手机,邮箱查重 API
    """
    serializer_class = CheckAPISerializer

    @staticmethod
    def check_info(phone_number=None,email=None):
        reply = {}
        if phone_number:
            phone_existed =  PhoneUser.objects.filter(phone_number=phone_number)
            if not phone_existed:
                reply['phone_existed'] = False
            else:
                reply['phone_existed'] = True
        if email:
            email_existed = PhoneUser.objects.filter(email=email)
            if not email_existed:
                reply['email_existed'] = False
            else:
                reply['email_existed'] = True
        return reply

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        email = serializer.validated_data['email']
        reply = self.check_info(phone_number,email)
        return Response(reply,HTTP_200_OK)


class SendMessageAPIView(APIView):
    """
    发送手机验证码
    """
    serializer_class = SendMessageSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        reply = send_message(phone_number)  # 发送验证码
        return Response(reply,HTTP_200_OK)


class PhoneUserCreateAPIView(APIView):
    """
    手机绑定
    """
    serializer_class = PhoneUserCreateSerializer
    def post(self,request):
        reply = {}
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        captcha = serializer.validated_data['captcha']
        email = serializer.validated_data.get('email')
        real_name = serializer.validated_data.get('real_name')
        # 先检验验证码
        if not verify(phone_number,captcha):
            reply['error_code'] = 1
            reply['data'] = {
                "phone_number":phone_number,
                "email":email,
                "real_name":real_name
            }
            return Response(reply,HTTP_400_BAD_REQUEST)
        else:
            try:
                p = PhoneUser.objects.create(user=request.user,phone_number=phone_number,
                                         email=email,real_name=real_name)
                p.save()
                reply['data'] = {
                    "phone_number": phone_number,
                    "email": email,
                    "real_name": real_name
                }
                return Response(reply,HTTP_201_CREATED)
            except:
                reply['error_code'] = 2
                return Response(reply,HTTP_400_BAD_REQUEST)

