from django.contrib import admin
from .models import Book,Refer,Holding,StarBook,ReadPlan,BrowsedBook,ImageFile
admin.site.register(Book)
admin.site.register(Refer)
admin.site.register(Holding)
admin.site.register(StarBook)
admin.site.register(ReadPlan)
admin.site.register(BrowsedBook)
admin.site.register(ImageFile)
# Register your models here.
