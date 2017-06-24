from django.contrib import admin
from .models import Book,Refer,Holding,StarBook,ReadPlan,BrowsedBook
admin.site.register(Book)
admin.site.register(Refer)
admin.site.register(Holding)
admin.site.register(StarBook)
admin.site.register(ReadPlan)
admin.site.register(BrowsedBook)
# Register your models here.
