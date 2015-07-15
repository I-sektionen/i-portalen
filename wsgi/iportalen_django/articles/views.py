from django.shortcuts import render
from .models import Article


def index(request):
    articles = Article.objects.all()
    print(articles)
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

def single_article(request, article_id):
    article = Article.objects.get(pk = article_id)
    return render(request, 'articles/article.html', {'article': article})