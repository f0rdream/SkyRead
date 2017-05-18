from django.conf.urls import include, url
url(r'^order/',include('order.urls',namespace='order')),
from django.conf.urls import include, url
from views import SearchView,BorrowHistory
urlpatterns = [
    url(r'^search/$',SearchView.as_view(),name='search'),
    url(r'^borrow/$',BorrowHistory.as_view(),name='borrow'),
]