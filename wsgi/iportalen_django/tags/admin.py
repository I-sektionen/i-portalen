from django.contrib import admin
from utils.admin import HiddenModelAdmin
from .models import Tag

# Register your models here.
admin.site.register(Tag, HiddenModelAdmin)
