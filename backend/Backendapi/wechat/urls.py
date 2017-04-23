from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$',views.wexin,name='wexin'),
    url(r'^connect/oauth2/authorize$',views.redict,name='auth'),
    url(r'^redict/$',views.redict,name="redict"),
]
