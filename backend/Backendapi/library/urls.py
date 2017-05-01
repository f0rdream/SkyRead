from django.conf.urls import url,include
from .views import BorrowItemView,BorrowItemDetailDeleteView
urlpatterns = [
    url(r'^borrow_items/$', BorrowItemView.as_view(), name='create_list'),
    url(r'^borrow_items/(?P<pk>\d+)',BorrowItemDetailDeleteView.as_view(),name='detail_delete'),
]