from django.utils import timezone
from django.template.loader_tags import register
import markdown as md
from articles.models import Article, Tag
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
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
def get_tags():
    tags = Tag.objects.all().order_by('name')
    return tags

@register.filter(is_safe=True)
@stringfilter
def markdown(text):
    return mark_safe(md.markdown(text))
