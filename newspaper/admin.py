from django.contrib import admin
from newspaper.models import Post,Category,Tag
# Register your models here.
admin.site.register([Post, Category, Tag])