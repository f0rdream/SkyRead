from django.conf.urls import url,include
from .views import (BorrowItemView,
                    BorrowItemDetailDeleteView,
                    BorrowQrCodeView,
                    VarifyAddToReturnBarView,
                    AddToReturnBarView,
                    ReturnItemView,
                    ReturnQrCodeView,
                    ReturnItemDetailDeleteView,
                    VarifyReturnBookBarView,
                    FinishReturnView,
                    OrderSuccessView,
                    SuccessOrderDetailView,
                    OrderWaitView,
                    WaitOrderDetailView)
urlpatterns = [
    url(r'^borrow/$', BorrowItemView.as_view(), name='borrow_create_list'),
    url(r'^borrow/(?P<pk>\d+)$',BorrowItemDetailDeleteView.as_view(),name='detail_delete'),
    url(r'^borrow/(?P<pk>\d+)/qrcode/$', BorrowQrCodeView.as_view(), name='get_borrow_qrcode'),
    url(r'^borrow/verify',VarifyAddToReturnBarView.as_view(),name='add'),
    url(r'^borrow/(?P<pk>\d+)/change_bar',AddToReturnBarView.as_view(),name='change_to_return_bar'),
    # return's urls
    url(r'^return/$',ReturnItemView.as_view(),name='return_list'),
    url(r'^return/(?P<pk>\d+)$',ReturnItemDetailDeleteView.as_view(),name='detail'),
    url(r'^return/(?P<pk>\d+)/qrcode/$', ReturnQrCodeView.as_view(), name='get_return_qrcode'),
    url(r'^return/verify',VarifyReturnBookBarView.as_view(),name='add'),
    url(r'^return/(?P<pk>\d+)/change_bar',FinishReturnView.as_view(),name='finish_return'),
    # order's urls
    url(r'^order/success/$',OrderSuccessView.as_view(),name='order_create_list'),
    url(r'^order/success/(?P<pk>\d+)$',SuccessOrderDetailView.as_view(),name='order_de'),
    url(r'^order/wait/$',OrderWaitView.as_view(),name='order_wait'),
    url(r'^order/wait/(?P<pk>\d+)$',WaitOrderDetailView.as_view(),name='wait_de'),

]