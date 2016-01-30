from itertools import chain
from django import template
from django.core.urlresolvers import reverse
from tags.models import Tag

register = template.Library()


@register.assignment_tag
def get_tags(user):
    free_tags = Tag.objects.filter(group__exact=None)

    user_tags = []
    user_groups = user.groups.all()
    for group in user_groups:
        user_tags = list(chain(group.tag_set.all(), user_tags))

    tags = list(chain(free_tags, user_tags))
    return tags


@register.assignment_tag
def get_menu_choices_tag(user):
    menu_choices = []
    if user.has_perm("tags.add_tag"):
        menu_choices.append(("Administrera taggar", reverse('admin:app_list', args=('tags',))))
    return menu_choices
