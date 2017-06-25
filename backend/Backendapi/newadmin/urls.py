from django.conf.urls import url,include
from .views import (test_perm,index,
                    create_admin_user,web_login,web_logout,
                    upload_excel,parse_the_excel,user_detail,
                    adminer_home,adminer_detail,money_home,book_home)
from android_views import (AndroidUserLoginAPIView,
                           is_login_view,
                           BorrowRecordView,ReturnRecordView,OrderRecordView,
                           AccountsInfoView,RecordSumView,SignItView,InfoView)
urlpatterns = [
    # urls for android admin
    url(r'^android_login/$',AndroidUserLoginAPIView.as_view()),
    url(r'^is_login/$',is_login_view),
    url(r'^record/borrow/$',BorrowRecordView.as_view()),
    url(r'^record/return/$',ReturnRecordView.as_view()),
    url(r'^record/order/$',OrderRecordView.as_view()),
    url(r'^sign/$',SignItView.as_view()),
    url(r'^info/$',InfoView.as_view()),
    # urls for web admin
    url(r'^test/$',test_perm),
    url(r'^index/$',index,name='newadmin_index'),
    url(r'^create_admin',create_admin_user,name='create_admin_user'),
    url(r'^login/$',web_login,name='web_login'),
    url(r'^logout/$',web_logout,name='web_logout'),
    url(r'^upload_file/$',upload_excel,name='upload_excel'),
    url(r'^read_file/$',parse_the_excel),
    url(r'^wechat_user/$',user_detail),
    url(r'^adminer_home',adminer_home,name='adminer_home'),
    url(r'^adminer_detail/(?P<user_id>\d+)$',adminer_detail,name='adminer_detail'),
    url(r'^money_home',money_home,name='money_home'),
    url(r'^book_home',book_home,name='book_home'),
]