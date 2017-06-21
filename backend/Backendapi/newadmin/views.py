# coding:utf-8
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from serializers import UserLoginSerializer
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import permission_required


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


def test_perm(request):
    user = request.user
    if user.has_perm('library.is_a_book_admin'):
        return HttpResponse('ok')
    else:
        return HttpResponse('你不是管理员')


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



