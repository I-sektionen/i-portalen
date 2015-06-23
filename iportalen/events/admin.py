from django.contrib import admin
from .models import Event, Entry, EntryDeadline

admin.site.register(Event)
admin.site.register(Entry)
admin.site.register(EntryDeadline)
