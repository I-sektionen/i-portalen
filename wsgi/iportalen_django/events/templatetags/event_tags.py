from organisations.models import Organisation
from django.template.loader_tags import register
from django.utils import timezone
from events.models import Event


@register.assignment_tag
def get_all_events():
    events = Event.objects.filter(
        status=Event.APPROVED,
        visible_from__lte=timezone.now(),
        end__gte=timezone.now()
    ).order_by('-start')
    return events


@register.assignment_tag
def get_event(pk):
    event = Event.objects.get(pk=pk)
    return event


@register.assignment_tag
def get_organisation_events(organisation_pk):
    event = Organisation.objects.get(pk=organisation_pk).event_set.filter(
        status=Event.APPROVED,
        visible_from__lte=timezone.now(),
        end__gte=timezone.now()
    )
    return event


@register.assignment_tag
def event_can_administer(event, user):
    return event.can_administer(user)
