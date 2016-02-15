from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
register = template.Library()


@register.assignment_tag
def get_menu_choices_tag(user):
    menu_choices = []
    if user.has_perm("tags.add_tag"):
        menu_choices.append((_("Administrera taggar"), reverse('iportalenadmin:app_list', args=('tags',))))
    return menu_choices
