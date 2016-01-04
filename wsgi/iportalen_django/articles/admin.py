from django.contrib import admin
from .models import Article
from utils.admin import HiddenModelAdmin

admin.site.register(Article, HiddenModelAdmin)
# Register your models here.
