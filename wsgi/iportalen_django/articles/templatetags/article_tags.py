from django.utils import timezone
from django.template.loader_tags import register
from articles.models import Article
from tags.models import Tag
from organisations.models import Organisation
from django import template

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
def get_organisation_articles(organisation_pk):
    articles = Organisation.objects.get(pk=organisation_pk).article_set.filter(
        approved=True,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now()
    )
    return articles
