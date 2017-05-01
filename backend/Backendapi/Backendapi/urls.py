from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
def homepage(request):
    response =  HttpResponse('login success')
    response.set_cookie(key=settings.SESSION_COOKIE_NAME,
                        value=request.session.session_key,
                        max_age=60 * 43200)
    return response
urlpatterns = [
    # Examples:
    # url(r'^$', 'demo1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^',include('wechat.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^homepage/',homepage,name='homepage'),
    url(r'^library/',include('library.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

