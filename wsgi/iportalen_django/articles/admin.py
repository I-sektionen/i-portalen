from django.contrib import admin
from .models import Article
import reversion

class ArticleAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Article, ArticleAdmin)
# Register your models here.
