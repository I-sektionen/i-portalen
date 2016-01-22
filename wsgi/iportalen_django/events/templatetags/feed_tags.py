from django.template.loader_tags import register
from events.models import Event

@register.assignment_tag()
def all_calendar_events():
    events = Event.objects.published()
    return events


@register.simple_tag()
def print_event(event):
    t_format = "%Y%m%dT%H%M%S"


    s = "BEGIN:VEVENT\n\
DTSTART:{start}\n\
DTEND:{end}\n\
SUMMARY:{summary}\n\
LOCATION:{location}\n\
DESCRIPTION:{desc}\n\
UID: {uid}\n\
END:VEVENT\n".format(start=event.start.strftime(t_format),
                     end=event.end.strftime(t_format),
                     summary=event.headline,
                     location=event.location,
                     desc=event.lead,
                     uid="IPORTALEN_DJANGO_1337" + event.pk)  # Unique identifier
    return s