from django.conf.urls import url,include
from .views import CommentView,InfoView
urlpatterns = [
    url(r'^amazon/info/(?P<isbn13>\d+)/$',CommentView.as_view()),
    url(r'^amazon/comments/(?P<isbn13>\d+)/$',InfoView.as_view()),
]