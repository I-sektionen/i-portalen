from django.contrib import admin

# Register your models here.
from speaker_list.models import SpeakerList
from utils.admin import iportalen_superadmin_site

iportalen_superadmin_site.register(SpeakerList)
