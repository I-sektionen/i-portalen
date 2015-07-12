from django.contrib import admin
from .models import Event, Entry, EntryDeadline
import reversion

class EventAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(Entry)
admin.site.register(EntryDeadline)
