from django import template
from django.template.loader_tags import register
from django.conf import settings
register = template.Library()

@register.assignment_tag
def is_debug():
    return settings.DEBUG


