# coding:utf-8
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from serializers import UserLoginSerializer
from django.contrib.auth import login, authenticate


def get_reply(code,msg):
    reply = dict()
    reply['error_code'] = code
    reply['msg'] = msg
    return reply
# Create your views here.


class AndroidUserLoginAPIView(APIView):
    """
    用户登录
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

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



