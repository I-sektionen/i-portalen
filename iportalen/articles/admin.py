from django.contrib import admin
from .models import Article, Tag

admin.site.register(Tag)
admin.site.register(Article)
# Register your models here.
