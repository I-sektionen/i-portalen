from utils.admin import iportalen_admin_site, iportalen_superadmin_site

from .models import Result

iportalen_admin_site.register(Result)

iportalen_superadmin_site.register(Result)
