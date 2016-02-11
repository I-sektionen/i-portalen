from django.template.loader_tags import register
from django.utils.translation import ugettext as _
#from pytz import timezone
from django.utils.timezone import timedelta
import socket

@register.simple_tag()
def print_event(event):
    def _descr(e):
        s1 = e.lead
        s2 = _(" Eventet finns på: www.i-portalen.se") + e.get_absolute_url()
        return s1 + s2
    t_format = "%Y%m%dT%H%M%SZ"  # Formating style used by the ics-file format. (Z means UTC).
    s = "".join(["BEGIN:VEVENT\n",
                 "DTSTART:{start}\n",
                 "DTEND:{end}\n",
                 "SUMMARY:{summary}\n",
                 "LOCATION:{location}\n",
                 "DESCRIPTION:{desc}\n",
                 "UID:{uid}\n",
                 "DTSTAMP:{timestamp}\n",
                 "LAST-MODIFIED:{modified}\n"
                 "URL:{url}\n",
                 "END:VEVENT\n"]).format(
        # This timezone thing does not work. Now is it converted manually by subtracting one hour to UTC.
 #       start=event.start.astimezone(timezone('Europe/London')).strftime(t_format),  # Switched to UTC instead.
 #       end=event.end.astimezone(timezone('Europe/London')).strftime(t_format),  # Switched to UTC instead.
        start=(event.start).strftime(t_format),
        end=(event.end).strftime(t_format),
        summary=event.headline,
        location=event.location,
        desc=_descr(event),
        url="www.i-portalen.se" + event.get_absolute_url(),
        uid="IPORTALEN_DJANGO_1337" + str(event.pk) + "@" + socket.gethostname(),  # Unique identifier
        modified=event.modified.strftime(t_format),
        timestamp=event.created.strftime(t_format))

    return s
