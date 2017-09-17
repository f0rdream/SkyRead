from django.contrib import admin
from .models import WeChatUser,PhoneUser,UserCreateBookList,BookInList,StarBookList
admin.site.register(WeChatUser)
admin.site.register(PhoneUser)
admin.site.register(UserCreateBookList)
admin.site.register(BookInList)
admin.site.register(StarBookList)
# Register your models here.
