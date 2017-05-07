# coding:utf-8
from django.conf.urls import url,include
from .views import UserProfileDetailAPIView,CheckAPIView,SendMessageAPIView,PhoneUserCreateAPIView

urlpatterns = [
    url(r'^$', UserProfileDetailAPIView.as_view(), name='user_detail'),  # 用户基本信息
    url(r'^check/$',CheckAPIView.as_view(),name='check_info'),  # 用户信息查重
    url(r'^send/$',SendMessageAPIView.as_view(),name='send message'),  # 发送手机验证码
    url(r'^phone/$',PhoneUserCreateAPIView.as_view(),name='create_phone')  # 绑定手机
]