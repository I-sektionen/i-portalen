from .models import Organisation, OrganisationPost
from utils.admin import HiddenModelAdmin, iportalen_admin_site

class OrganisationsAdmin(HiddenModelAdmin):
    readonly_fields =("modified_by",)

class OrganisationsPostAdmin(HiddenModelAdmin):
    readonly_fields =("modified_by",)

iportalen_admin_site.register(Organisation, OrganisationsAdmin)
iportalen_admin_site.register(OrganisationPost, OrganisationsPostAdmin)
