from django.contrib import admin
from newspaper.models import Post,Category,Tag, Contact, UserProfile, Comment, Newsletter
# Register your models here.
#admin.site.register(Post)
#admin.site.register(Category)
#admin.site.register(Tag)
admin.site.register([Post, Category, Tag, Contact, UserProfile, Comment, Newsletter])