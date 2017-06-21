from django.conf.urls import url,include
from .views import (AndroidUserLoginAPIView,test_perm)
urlpatterns = [
    url(r'^android_login/$',AndroidUserLoginAPIView.as_view()),
    url(r'^test/$',test_perm)
]