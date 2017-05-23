from django.conf.urls import url,include
from .views import (DoubanReadingListView,
                    DoubanReadingDetailView,
                    DoubanCommentListView,
                    DoubanCommentDetailView,
                    DoubanReviewListView,
                    DoubanReviewDetailView,)
urlpatterns = [
    url(r'^comments/(?P<isbn13>\d+)/$',DoubanCommentListView.as_view()),
    url(r'^comments/id/(?P<pk>\d+)/$',DoubanCommentDetailView.as_view()),
    url(r'^pre/(?P<isbn13>\d+)/$', DoubanReadingListView.as_view()),
    url(r'^pre/id/(?P<pk>\d+)/$', DoubanReviewDetailView.as_view()),
    url(r'^reviews/(?P<isbn13>\d+)/$', DoubanReviewListView.as_view()),
    url(r'^reviews/id/(?P<pk>\d+)/$', DoubanReviewDetailView.as_view()),
]