from django.conf.urls import url,include
from views import TagBookListView,AuthorBookListView,RecommandView
urlpatterns = [
    url(r'^tag/$',TagBookListView.as_view()),
    url(r'^author/$',AuthorBookListView.as_view()),
    url(r'^recommand/$',RecommandView.as_view()),
]