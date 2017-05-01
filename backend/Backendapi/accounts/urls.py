from django.conf.urls import url,include
from .views import UserProfileDetailAPIView


urlpatterns = [
    url(r'^user_detail/$', UserProfileDetailAPIView.as_view(), name='user_detail'),
]