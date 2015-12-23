from django.contrib import admin
from .models import Event, EntryAsPreRegistered, EntryAsReserve, EntryAsParticipant

admin.site.register(Event)
admin.site.register(EntryAsPreRegistered)
admin.site.register(EntryAsReserve)
admin.site.register(EntryAsParticipant)
