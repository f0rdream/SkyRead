# coding:utf-8
from django.conf.urls import url,include
from .views import (UserProfileDetailAPIView,
                    CheckAPIView, SendMessageAPIView,
                    PhoneUserCreateAPIView, OrderMessageOpenOrClose,
                    ReturnMessageOpenOrClose, FeedBackView,
                    ChangeTimeView, AddLabelView,DeleteLabelView,
                    BookListView, StarBookListView, BookListDetailView,
                    CycleView, CycleSearchView,CycleListCommentView,
                    CycleNoteCommentView)

urlpatterns = [
    url(r'^$', UserProfileDetailAPIView.as_view(), name='user_detail'),  # 用户基本信息
    url(r'^check/$',CheckAPIView.as_view(),name='check_info'),  # 用户信息查重
    url(r'^send/$',SendMessageAPIView.as_view(),name='send message'),  # 发送手机验证码
    url(r'^phone/$',PhoneUserCreateAPIView.as_view(),name='create_phone'),  # 绑定手机
    url(r'^return_msg/$',ReturnMessageOpenOrClose.as_view(),name='return_msg'), # 开关消息
    url(r'^order_msg/$',OrderMessageOpenOrClose.as_view(),name='order_msg'), # 开关消息
    url(r'^change_times/$',ChangeTimeView.as_view(),name='change_time'),  # 更改推荐频率
    url(r'^feedback/$', FeedBackView.as_view(), name='feedback'),  # 反馈
    url(r'^label/$', AddLabelView.as_view()),  # 自己添加的系统分类
    url(r'^label/(?P<pk>\d+)$', DeleteLabelView.as_view()),  # 自己添加的系统分类
    url(r'^book_list/$', BookListView.as_view()),  # 用户自建书单
    url(r'^book_list/star/$', StarBookListView.as_view()),  # 用户收藏的书单
    url(r'^book_list/(?P<pk>\d+)/$', BookListDetailView.as_view()),  # 书单详情
    url(r'^cycle/(?P<page>\d+)/$', CycleView.as_view()),
    url(r'^cycle/search/$',CycleSearchView.as_view()),
    url(r'^cycle/list_comment/(?P<pk>\d+)/$', CycleListCommentView.as_view()),  # 书单评论
    url(r'^cycle/note_comment/(?P<pk>\d+)/$', CycleNoteCommentView.as_view()),  # 笔记评论
]