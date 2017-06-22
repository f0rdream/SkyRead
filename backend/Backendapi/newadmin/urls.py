from django.conf.urls import url,include
from .views import (test_perm,index,
                    create_admin_user,web_login,web_logout)
from android_views import (AndroidUserLoginAPIView,
                           is_login_view,
                           BorrowRecordView,ReturnRecordView,OrderRecordView,
                           AccountsInfoView,RecordSumView)
urlpatterns = [
    # urls for android admin
    url(r'^android_login/$',AndroidUserLoginAPIView.as_view()),
    url(r'^is_login/$',is_login_view),
    url(r'^record/borrow/$',BorrowRecordView.as_view()),
    url(r'^record/return/$',ReturnRecordView.as_view()),
    url(r'^record/order/$',OrderRecordView.as_view()),
    url(r'^record/sum/$',RecordSumView.as_view()),
    url(r'^accounts/$',AccountsInfoView.as_view()),
    # urls for web admin
    url(r'^test/$',test_perm),
    url(r'^index/$',index),
    url(r'^create_admin',create_admin_user,name='create_admin_user'),
    url(r'^login/$',web_login,name='web_login'),
    url(r'^logout/$',web_logout,name='web_logout'),
]