from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from utils.admin import HiddenModelAdmin, iportalen_admin_site

# Register your models here.
iportalen_admin_site.register(Group, HiddenModelAdmin)
iportalen_admin_site.register(Site, HiddenModelAdmin)
