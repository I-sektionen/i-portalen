from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from django.utils.translation import ugettext as _

from user_managements.models import IUser


@register.assignment_tag
def get_user_from_id(user_id):
    return IUser.objects.get(pk=user_id)

@register.assignment_tag
def get_menu_choices_user(user):
    menu_choices = []

    if user.has_perm("user_managements.add_iuser"):
        menu_choices.append((_("Lägg till Liu-idn i whitelist"), reverse('user_management:add users to whitelist')))

    if user.has_perm('user_managements.can_view_users'):
        menu_choices.append((_('Alla användare'), reverse('user_management:all users')))

    if user.has_perm('user_managements.can_view_subscribers'):
        menu_choices.append((_('Lista Ipikuréprenumeranter'), reverse('user_management:ipikure subscribers')))

    return menu_choices
