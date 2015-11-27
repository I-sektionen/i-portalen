from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from utils.markdown import markdown_to_html
register = template.Library()


@register.assignment_tag
def is_debug():
    return settings.DEBUG


@register.filter(is_safe=True)
@stringfilter
def markdown(text):
    return mark_safe(markdown_to_html(text))
