from django.contrib import admin
from .models import WeChatUser,PhoneUser,UserCreateBookList,BookInList
admin.site.register(WeChatUser)
admin.site.register(PhoneUser)
admin.site.register(UserCreateBookList)
admin.site.register(BookInList)
# Register your models here.
