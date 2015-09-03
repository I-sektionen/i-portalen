from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm


def create_or_modify_article(request, article_id=None):
    a = None
    if article_id:
        a = Article.objects.get(pk=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=a)
        # check whether it's valid:
        if form.is_valid():
            a = form.save()
            return redirect(a)

    else:
        form = ArticleForm(instance=a)
        return render(request, 'articles/article_form.html', {'form': form})


def single_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    return render(request, 'articles/article.html', {'article': article})

def all_articles(request):
    articles = Article.objects.all()
    return render(request, 'articles/articles.html', {'articles': articles})

def all_approved_articles(request):
    articles = Article.objects.filter(approved=True)
    return render(request, 'articles/articles.html', {'articles': articles})

def all_unapproved_articles(request):
    articles = Article.objects.filter(approved=False)
    return render(request, 'articles/articles.html', {'articles': articles})

def approve_article(request, article_id):
    a = Article.objects.get(pk=article_id)
    a.approved = True
    a.save()
    return redirect(a)
