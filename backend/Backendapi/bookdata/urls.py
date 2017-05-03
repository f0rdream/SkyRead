from django.conf.urls import url,include
from .views import (BookInfoView)
urlpatterns = [
    url(r'^isbn/(?P<isbn13>\d+)$',BookInfoView.as_view(),name='book'),
]