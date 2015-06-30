__author__ = 'jonathan'
from django.template.loader_tags import register
from django.utils import timezone
from events.models import Event

@register.assignment_tag
def get_all_events():
    events = Event.objects.filter(
        approved=True,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now()
    ).order_by('-modified')
    return events

@register.assignment_tag
def get_event(pk):
    event = Event.objects.get(pk=pk)
    return event

