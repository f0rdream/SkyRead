from django.conf.urls import url,include
from views import TagBookListView,AuthorBookListView,RecommendView,SameUserBookList,\
    SameUserBookDetail, PositionView, NearByBookView
urlpatterns = [
    url(r'^tag/(?P<page>\d+)/$',TagBookListView.as_view()),
    url(r'^author/(?P<page>\d+)/$',AuthorBookListView.as_view()),
    url(r'^recommend/$',RecommendView.as_view()),
    url(r'^user_like/$',SameUserBookList.as_view()),
    url(r'^user_like/(?P<order>\d+)/$',SameUserBookDetail.as_view()),
    url(r'^position/$', PositionView.as_view()),
    url(r'^nearby/$', NearByBookView.as_view()),
]