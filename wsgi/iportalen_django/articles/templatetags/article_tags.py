from django.utils import timezone
from django.template.loader_tags import register
import markdown as md
from articles.models import Article
from tags.models import Tag
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


@register.filter(is_safe=True)
@stringfilter
def markdown(text):
    text = re.sub(r'([#]{2,})', '#', text)
    text = re.sub(r'([=]{3,})', '', text)
    text = re.sub(r'([-]{3,})', '', text)
    text = re.sub(r'([`])', '', text)

    text = md.markdown(text, safe_mode='escape', output_format='html5').replace("<hr>", "")
    return mark_safe(text)


@register.assignment_tag
def get_user_articles(user):
    approved_articles = user.article_set.filter(approved=True, visible_to__gte=timezone.now())
    unapproved_articles = user.article_set.filter(approved=False, draft=False, visible_to__gte=timezone.now())
    draft_articles = user.article_set.filter(draft=True, visible_to__gte=timezone.now())

    return {'approved_articles':approved_articles, 'unapproved_articles':unapproved_articles, 'draft_articles':draft_articles}

@register.assignment_tag
def select_tag_status(article_id, tag_id):
    if article_id == None:
        return ""
    elif Tag.objects.get(pk=tag_id) in Article.objects.get(pk=article_id).tags.all():
        return "selected"
    else:
        return ""