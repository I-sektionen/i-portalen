from django.shortcuts import render
from .models import Article

def single_article(request, article_id):
    article = Article.objects.get(pk = article_id)
    return render(request, 'articles/article.html', {'article': article})
