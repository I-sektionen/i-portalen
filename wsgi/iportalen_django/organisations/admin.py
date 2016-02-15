from .models import Organisation, OrganisationPost
from utils.admin import HiddenModelAdmin, iportalen_admin_site, iportalen_superadmin_site
from django.contrib import admin


class OrganisationsAdmin(HiddenModelAdmin):
    readonly_fields = ("modified_by",)


class OrganisationsPostAdmin(HiddenModelAdmin):
    readonly_fields = ("modified_by",)

iportalen_admin_site.register(Organisation, OrganisationsAdmin)
iportalen_admin_site.register(OrganisationPost, OrganisationsPostAdmin)

iportalen_superadmin_site.register(Organisation)
iportalen_superadmin_site.register(OrganisationPost)
