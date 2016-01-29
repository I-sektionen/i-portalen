from .models import Event, EntryAsPreRegistered, EntryAsReserve, EntryAsParticipant
from utils.admin import iportalen_admin_site

iportalen_admin_site.register(Event)
iportalen_admin_site.register(EntryAsPreRegistered)
iportalen_admin_site.register(EntryAsReserve)
iportalen_admin_site.register(EntryAsParticipant)
