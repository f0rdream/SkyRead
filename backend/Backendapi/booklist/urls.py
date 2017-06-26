from django.conf.urls import url,include
from views import TagBookListView,AuthorBookListView,RecommandView
urlpatterns = [
    url(r'^tag/(?P<page>\d+)/$',TagBookListView.as_view()),
    url(r'^author/(?P<page>\d+)/$',AuthorBookListView.as_view()),
    url(r'^recommand/$',RecommandView.as_view()),
]