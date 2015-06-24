__author__ = 'jonathan'
from django.template.loader_tags import register

from articles.models import Article

@register.assignment_tag
def get_articles():
    articles = Article.objects.all()
    return articles