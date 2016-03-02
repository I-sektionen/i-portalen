from django.contrib import admin
from .models import Hero
from utils.admin import iportalen_admin_site, iportalen_superadmin_site


class HeroAdmin(admin.ModelAdmin):
    readonly_fields = ('file_name', 'modified_by')

    def save_model(self, request, obj, form, change):
        """
        Update modified-by fields.

        The date fields are updated at the model layer, but that's not got
        access to the user.
        """

        obj.modified_by = request.user

        # Let the superclass do the final saving.
        return super(HeroAdmin, self).save_model(request, obj, form, change)

iportalen_admin_site.register(Hero, HeroAdmin)

iportalen_superadmin_site.register(Hero)
