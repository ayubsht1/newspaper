from django.contrib import admin
from newspaper.models import Post,Category,Tag, Contact, UserProfile, Comment, Newsletter
# Register your models here.
#admin.site.register(Post)
#admin.site.register(Category)
#admin.site.register(Tag)
admin.site.register([Category, Tag, Contact, UserProfile, Comment, Newsletter])

from django_summernote.admin import SummernoteModelAdmin
from .models import Post

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)