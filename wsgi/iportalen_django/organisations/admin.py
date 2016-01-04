from django.contrib import admin
from .models import Organisation, OrganisationPost
from utils.admin import HiddenModelAdmin
# Register your models here.
admin.site.register(Organisation, HiddenModelAdmin)
admin.site.register(OrganisationPost, HiddenModelAdmin)
