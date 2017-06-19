from django.conf.urls import url,include
from .views import (BookInfoView,Serach,ReferBookView,HoldingView,GuideBookView,
                    StarBookView,StarBookDetailView,CommentView,ReadPlanView,ReadPlanDetailView)
urlpatterns = [
    url(r'^isbn/(?P<isbn13>\d+)$',BookInfoView.as_view(),name='book'),
    url(r'^search/$',Serach.as_view()),
    url(r'^refer/(?P<isbn13>\d+)$',ReferBookView.as_view(),name='refer'),
    url(r'^comments/(?P<isbn13>\d+)/$',CommentView.as_view()),
    url(r'^collection/(?P<isbn13>\d+)$',HoldingView.as_view(),name='holding'),
    url(r'^starbook/$',StarBookView.as_view(),name='starbook'),
    url(r'^guide/(?P<guide_id>\d+)/(?P<page>\d+)$', GuideBookView.as_view(), name='refer'),
    url(r'^starbook/(?P<pk>\d+)$',StarBookDetailView.as_view(),name='star_detail'),
    url(r'^readplan/$',ReadPlanView.as_view(),name='read_plan'),
    url(r'^readplan/(?P<pk>\d+)$',ReadPlanDetailView.as_view(),name='read_plan_detail'),
]