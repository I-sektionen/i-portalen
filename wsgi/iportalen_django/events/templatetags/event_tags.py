__author__ = 'jonathan'
from django.template.loader_tags import register
from django.utils import timezone
from events.models import Event
from tags.models import Tag

@register.assignment_tag
def get_all_events():
    events = Event.objects.filter(
        approved=True,
        visible_from__lte=timezone.now(),
        end__gte=timezone.now()
    ).order_by('-modified')
    return events

@register.assignment_tag
def get_event(pk):
    event = Event.objects.get(pk=pk)
    return event

@register.assignment_tag
def get_group_events(group_pk):
    tags = Tag.objects.filter(group=group_pk).distinct().values('pk')
    event = Event.objects.filter(
        tags__in=tags,
        approved=True,
        visible_from__lte=timezone.now(),
        end__gte=timezone.now()
    )
    return event