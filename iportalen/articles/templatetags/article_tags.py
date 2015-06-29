from django.utils import timezone
from django.template.loader_tags import register

from articles.models import Article

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
    article = Article.objects.get(pk=pk)
    return article
