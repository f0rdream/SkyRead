from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    url(r'^wexin$',views.wexin,name='wexin'),
    url(r'^connect/oauth2/authorize$',views.redict,name='auth'),
    url(r'^$',views.redict,name="redict"),
    url(r'^test_page/$',views.test_page,name="test"),
    url(r'^signature/$',views.Sign.as_view())
]
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)