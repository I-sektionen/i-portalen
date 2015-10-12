from django.utils import timezone
from django.template.loader_tags import register
from articles.models import Article
from tags.models import Tag
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from utils.markdown import markdown_to_html

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


@register.filter(is_safe=True)
@stringfilter
def markdown(text):
    return mark_safe(markdown_to_html(text))


@register.assignment_tag
def get_user_articles(user):
    return Article.objects.get_user_articles(user)

@register.assignment_tag
def select_tag_status(article_id, tag_id):
    if article_id == None:
        return ""
    elif Tag.objects.get(pk=tag_id) in Article.objects.get(pk=article_id).tags.all():
        return "selected"
    else:
        return ""

@register.assignment_tag
def get_group_articles(group_pk):
    tags = Tag.objects.filter(group=group_pk).distinct().values('pk')
    articles = Article.objects.filter(
        tags__in=tags,
        approved=True,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now()
    )
    return articles
