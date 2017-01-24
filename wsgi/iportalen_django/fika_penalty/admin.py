from fika_penalty.models import FikaPenalty
from utils.admin import iportalen_admin_site, iportalen_superadmin_site

iportalen_admin_site.register(FikaPenalty)

iportalen_superadmin_site.register(FikaPenalty)
