from django.core.urlresolvers import reverse
from organisations.models import Organisation
from django.template.loader_tags import register
from django.utils import timezone
from events.models import Event
from django.utils.translation import ugettext as _


@register.assignment_tag
def get_all_events():
    events = Event.objects.published()
    return events


@register.assignment_tag
def get_event(event, user):
    can_administer = event.can_administer(user)
    if event.status == Event.APPROVED or can_administer:
        return {
            "can_administer": can_administer,
            "registered": event.registered(user),
        }
    else:
        return None


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


@register.assignment_tag
def event_is_checked_in(event, user):
    return event.is_checked_in(user)


@register.assignment_tag
def event_reserve(event, user):
    return event.reserve(user)


@register.assignment_tag
def event_reserve_nr(event, user):
    return event.reserve_nr(user)


@register.assignment_tag
def get_menu_choices_event(user):
    menu_choices = []
    if Event.objects.user(user).count() != 0:
        menu_choices.append((_('Mina event'), reverse('events:by user')))
    menu_choices.append((_('Skapa ett event'), reverse('events:create')))
    if user.has_perm("events.can_approve_event"):
        menu_choices.append((_('Godkänn Event'), reverse('events:unapproved')))  # With perm to edit events.
    if user.has_perm("events.can_view_no_shows"):
        menu_choices.append((_('Visa No Shows'), reverse('events:no_shows')))
    return menu_choices


@register.assignment_tag
def _or(*args):
    temp = False
    for v in args:
        if v:
            temp = True
    return temp
