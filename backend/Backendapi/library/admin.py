from django.contrib import admin
from .models import BorrowItem,SuccessOrderItem,WaitOrderItem,PayItem
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(BorrowItem)
admin.site.register(Permission)
admin.site.register(SuccessOrderItem)
admin.site.register(WaitOrderItem)
admin.site.register(PayItem)