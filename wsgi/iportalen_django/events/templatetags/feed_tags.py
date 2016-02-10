from django.template.loader_tags import register
from django.utils.translation import ugettext as _
from pytz import timezone


@register.simple_tag()
def print_event(event):
    def _descr(e):
        s1 = e.lead
        s2 = _(" Eventet finns på: www.i-portalen.se") + e.get_absolute_url()
        return s1 + s2
    t_format = "%Y%m%dT%H%M%SZ"  # Formating style used by the ics-file format.
    s = "".join(["BEGIN:VEVENT\n",
                 "DTSTART:{start}\n",
                 "DTEND:{end}\n",
                 "SUMMARY:{summary}\n",
                 "LOCATION:{location}\n",
                 "DESCRIPTION:{desc}\n",
                 "UID: {uid}\n",
                 "URL:{url}\n",
                 "END:VEVENT\n"]).format(
        start=event.start.astimezone(timezone('Europe/Stockholm')).strftime(t_format),
        end=event.end.astimezone(timezone('Europe/Stockholm')).strftime(t_format),
        summary=event.headline,
        location=event.location,
        desc=_descr(event),
        url="www.i-portalen.se" + event.get_absolute_url(),
        uid="IPORTALEN_DJANGO_1337" + str(event.pk))  # Unique identifier
    return s
