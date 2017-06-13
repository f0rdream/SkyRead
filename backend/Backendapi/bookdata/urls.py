from django.conf.urls import url,include
from .views import (BookInfoView,Serach,ReferBookView,HoldingView)
urlpatterns = [
    url(r'^isbn/(?P<isbn13>\d+)$',BookInfoView.as_view(),name='book'),
    url(r'^search/$',Serach.as_view()),
    url(r'^refer/(?P<isbn13>\d+)$',ReferBookView.as_view(),name='refer'),
    url(r'^collection/(?P<isbn13>\d+)$',HoldingView.as_view(),name='holding')
]