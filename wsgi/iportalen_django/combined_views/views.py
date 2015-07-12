from django.http import HttpResponse
from django.shortcuts import render
from articles.models import Article


def index(request):
    articles = Article.objects.all()
    print(articles)
    context = {'articles': articles}
    return render(request, 'combined_views/index.html', context)