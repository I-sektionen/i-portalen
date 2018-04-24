from django.contrib import admin
from .models import Alumni_Article, Magazine
from utils.admin import HiddenModelAdmin, iportalen_admin_site, iportalen_superadmin_site


iportalen_admin_site.register(Alumni_Article)
iportalen_superadmin_site.register(Alumni_Article)

iportalen_admin_site.register(Magazine)
iportalen_superadmin_site.register(Magazine)
