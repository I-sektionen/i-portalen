from django.template.loader_tags import register
from django.conf import settings


@register.assignment_tag
def in_debug():
    return settings.DEBUG


