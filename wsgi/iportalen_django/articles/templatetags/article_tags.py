from itertools import chain
from django.utils import timezone
from django.template.loader_tags import register
import markdown as md
from articles.models import Article, Tag
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.assignment_tag
def get_all_articles():
    articles = Article.objects.filter(
        approved=True,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now()
    ).order_by('-modified')
    return articles


@register.assignment_tag
def get_article(pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        article = None
    return article


@register.assignment_tag
def get_tags(user):
    free_tags = Tag.objects.filter(group__exact=None)

    user_tags = []
    user_groups = user.groups.all()
    for group in user_groups:
        user_tags = list(chain(group.tag_set.all(), user_tags))

    tags = list(chain(free_tags, user_tags))
    return tags


@register.filter(is_safe=True)
@stringfilter
def markdown(text):
    text = re.sub(r'([#]{2,})', '#', text)
    text = re.sub(r'([=]{3,})', '', text)
    text = re.sub(r'([-]{3,})', '', text)
    text = re.sub(r'([`])', '', text)

    text = md.markdown(text, safe_mode='escape', output_format='html5').replace("<hr>", "")
    return mark_safe(text)
