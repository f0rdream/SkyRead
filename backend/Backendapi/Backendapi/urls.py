# coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static


def homepage(request):
    response = HttpResponse('login success')
    response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                        value=request.session.session_key,
                        max_age=60 * 43200)
    return response

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('wechat.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^homepage/', homepage,name='homepage'),
    url(r'^library/', include('library.urls')),
    url(r'^book/', include('bookdata.urls')),
    url(r'^douban/', include('douban.urls')),
    # url(r'^amazon/', include('douban.urls')),
    url(r'^history/', include('history.urls')),
    url(r'^web/', include('newadmin.urls')),
    url(r'^list/', include('booklist.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


