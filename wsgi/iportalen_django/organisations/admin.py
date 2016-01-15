from django.contrib import admin
from .models import Organisation, OrganisationPost
from utils.admin import HiddenModelAdmin, iportalen_admin_site
# Register your models here.
iportalen_admin_site.register(Organisation, HiddenModelAdmin)
iportalen_admin_site.register(OrganisationPost, HiddenModelAdmin)
