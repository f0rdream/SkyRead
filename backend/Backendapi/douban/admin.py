from django.contrib import admin
from .models import Comment,Reading,Review
# Register your models here.
admin.site.register(Comment)
admin.site.register(Reading)
admin.site.register(Review)