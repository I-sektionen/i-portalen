from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from django.utils.translation import ugettext as _


@register.assignment_tag
def get_menu_choices_exchange_portal(user):
    menu_choices = []
    if user.has_perm("exchange_portal.add_school"):
        menu_choices.append((_("Administrera Utlandsportalen"), reverse('iportalenadmin:app_list', args=('exchange_portal',))))
    return menu_choices



@register.assignment_tag
def has_perm_exchange_portal(user):
    if user.has_perm("exchange_portal.add_school"):
        return True
    else:
        return False
