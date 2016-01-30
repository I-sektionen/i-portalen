from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.assignment_tag
def get_menu_choices_tag(user):
    menu_choices = []
    if user.has_perm("tags.add_tag"):
        menu_choices.append(("Administrera taggar", reverse('admin:app_list', args=('tags',))))
    return menu_choices
