from django.contrib import admin
from .models import Article, Tag
import reversion

class ArticleAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
# Register your models here.
