from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from .models import Article, Tag
from .forms import ArticleForm

def create_or_modify_article(request, article_id=None):
    if request.user.is_authenticated():
        a = None
        if article_id:
            a = Article.objects.get(pk=article_id)
            if not a.user == request.user and not request.user.has_perm("articles.change_article"):
                # hasn't permission to change
                return HttpResponseForbidden()

        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=a)

            # check whether it's valid:
            if form.is_valid():
                a = form.save(commit=False)
                if not request.user.has_perm("articles.can_approve_article"):
                    a.approved = False
                if hasattr(a, "user"):
                    a.save()
                else:
                    a.user = request.user
                    a.save()
                form.save_m2m()
                return redirect(a)

        else:
            form = ArticleForm(instance=a)
            return render(request, 'articles/article_form.html', {'form': form})
    else:
        # Error not logged in
        return HttpResponseForbidden()



def single_article(request, article_id):
    article = Article.objects.get(pk=article_id, approved=True)
    return render(request, 'articles/article.html', {'article': article})

def all_articles(request):
    articles = Article.objects.all(approved=True)
    return render(request, 'articles/articles.html', {'articles': articles})

def all_approved_articles(request):
    articles = Article.objects.filter(approved=True)
    return render(request, 'articles/articles.html', {'articles': articles})

def all_unapproved_articles(request):
    articles = Article.objects.filter(approved=False, draft=False)
    return render(request, 'articles/articles.html', {'articles': articles})

def approve_article(request, article_id):
    a = Article.objects.get(pk=article_id)
    if a.draft:
        # cant publish article in draft state
        return HttpResponseForbidden()
    a.approved = True
    a.save()
    return redirect(a)

def articles_by_tag(request, tag_name):
    articles = Tag.objects.get(name=tag_name).article_set.all(approved=True)
    return render(request, 'articles/articles.html', {'articles': articles})

def articles_by_user(request):
    articles = request.user.article_set.all()
    return render(request, 'articles/articles.html', {'articles': articles})
