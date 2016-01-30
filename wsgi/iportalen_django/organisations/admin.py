from .models import Organisation, OrganisationPost
from utils.admin import HiddenModelAdmin, iportalen_admin_site

iportalen_admin_site.register(Organisation, HiddenModelAdmin)
iportalen_admin_site.register(OrganisationPost, HiddenModelAdmin)
