from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils import timezone
from django.utils.safestring import mark_safe

from articles.models import Article
from events.models import Event
from utils.markdown import markdown_to_html
register = template.Library()


@register.assignment_tag
def is_debug():
    return settings.DEBUG


@register.filter(is_safe=True)
@stringfilter
def markdown(text):
    return mark_safe(markdown_to_html(text))


@register.assignment_tag
def get_menu_choices_iportalen(self):
    menu_choices = []  # List of extra menu choices.
    if self.is_staff:
        menu_choices.append(('Adminsidan', '/admin'))  # Staff users who can access Admin page.
    return menu_choices


@register.assignment_tag
def get_sponsored_content():
    content_feed_list = list(Article.objects.published().filter(sponsored=True).order_by('-visible_from'))
    content_feed_list += list(Event.objects.published().filter(sponsored=True).order_by('-visible_from'))

    return sorted(content_feed_list, key=lambda contents: contents.visible_from, reverse=False)
