from django.conf.urls import url,include
from .views import (BorrowItemView,
                    BorrowItemDetailDeleteView,
                    BorrowQrCodeView,
                    ManyBorrowQrCodeView,
                    VarifyAddToReturnBarView,
                    AddToReturnBarView,
                    ReturnItemView,
                    ReturnQrCodeView,
                    ManyReturnQrCodeView,
                    ReturnItemDetailDeleteView,
                    VarifyReturnBookBarView,
                    FinishReturnView,
                    OrderSuccessView,
                    SuccessOrderDetailView,
                    OrderWaitView,
                    WaitOrderDetailView,
                    CurlListView,
                    qrcode_info,
                    PayView,
                    PayItView,
                    ConfirmIt,
                    AdminConfirmInfo)
urlpatterns = [
    url(r'^borrow/$', BorrowItemView.as_view(), name='borrow_create_list'),
    url(r'^borrow/(?P<pk>\d+)$',BorrowItemDetailDeleteView.as_view(),name='detail_delete'),
    url(r'^borrow/qrcode/$', ManyBorrowQrCodeView.as_view(), name='get_borrow_qrcode'),
    url(r'^borrow/verify',VarifyAddToReturnBarView.as_view(),name='add'),
    url(r'^borrow/change_bar',AddToReturnBarView.as_view(),name='change_to_return_bar'),
    # return's urls
    url(r'^return/$',ReturnItemView.as_view(),name='return_list'),
    url(r'^return/(?P<pk>\d+)$',ReturnItemDetailDeleteView.as_view(),name='detail'),
    url(r'^return/qrcode/$', ManyReturnQrCodeView.as_view(), name='get_return_qrcode'),
    url(r'^return/verify',VarifyReturnBookBarView.as_view(),name='add'),
    url(r'^return/change_bar',FinishReturnView.as_view(),name='finish_return'),
    # order's urls
    url(r'^order/success/$',OrderSuccessView.as_view(),name='order_create_list'),
    url(r'^order/success/(?P<pk>\d+)$',SuccessOrderDetailView.as_view(),name='order_de'),
    url(r'^order/wait/$',OrderWaitView.as_view(),name='order_wait'),
    url(r'^order/wait/(?P<pk>\d+)$',WaitOrderDetailView.as_view(),name='wait_de'),
    url(r'^curl/$',CurlListView.as_view()),
    # qrcode_info
    url(r'^qrcode_info/$',qrcode_info,name='get_qrcode_info'),
    # pay's urls
    url(r'^pay_info/(?P<pay_id>\d+)$', PayView.as_view(), name='get_pay_info'),
    url(r'^pay/(?P<pay_id>\d+)$',PayItView.as_view(),name='pay_it'),
    url(r'^confirm_info/(?P<pay_id>\d+)$',AdminConfirmInfo.as_view(),name='confirm info'),
    url(r'^confirm/(?P<pay_id>\d+)$',ConfirmIt.as_view(),name='confirm_it')
]
