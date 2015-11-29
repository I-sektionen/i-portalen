from django.contrib import admin
from .models import Event, EntryAsPreRegistered, EntryAsReserve, EntryAsParticipant
from reversion.admin import VersionAdmin


class EventAdmin(VersionAdmin):
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(EntryAsPreRegistered)
admin.site.register(EntryAsReserve)
admin.site.register(EntryAsParticipant)
