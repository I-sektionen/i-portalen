from django.shortcuts import render
from .models import Article


def index(request):
    articles = Article.objects.all()
    print(articles)
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)
