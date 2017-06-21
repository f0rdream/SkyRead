from django.conf.urls import url,include
from .views import (AndroidUserLoginAPIView,test_perm,is_login_view)
urlpatterns = [
    url(r'^android_login/$',AndroidUserLoginAPIView.as_view()),
    url(r'^is_login/$',is_login_view),
    url(r'^test/$',test_perm)
]