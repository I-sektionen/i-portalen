from django.contrib import admin
from .models import Article
from reversion.admin import VersionAdmin


class ArticleAdmin(VersionAdmin):
    pass

admin.site.register(Article, ArticleAdmin)
# Register your models here.
