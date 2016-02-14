from utils.admin import HiddenModelAdmin, iportalen_admin_site
from django.contrib import admin

from .models import Tag

# Register your models here.
iportalen_admin_site.register(Tag, HiddenModelAdmin)
admin.site.register(Tag)
