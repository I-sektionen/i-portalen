from itertools import chain
from django.template.loader_tags import register
from django import template
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