from django.conf.urls import url,include
from .views import (AndroidUserLoginAPIView)
urlpatterns = [
    url(r'^android_login/$',AndroidUserLoginAPIView.as_view())
]