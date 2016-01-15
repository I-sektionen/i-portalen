from django.contrib import admin
from .models import Article
from utils.admin import HiddenModelAdmin, iportalen_admin_site

iportalen_admin_site.register(Article, HiddenModelAdmin)
# Register your models here.
