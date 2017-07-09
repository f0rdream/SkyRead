from django.contrib import admin
from .models import AdminBorrowItemRecord,Admin_Permission,ExcelFile,Sign,Picture
admin.site.register(AdminBorrowItemRecord)
admin.site.register(Admin_Permission)
# Register your models here.
admin.site.register(ExcelFile)
admin.site.register(Sign)
admin.site.register(Picture)