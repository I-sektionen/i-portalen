from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Article, Tag
from .forms import ArticleForm


@login_required()
def create_or_modify_article(request, article_id=None):
    if request.user.is_authenticated():
        a = None
        if article_id:
            a = Article.objects.get(pk=article_id)
            if not a.user == request.user and not request.user.has_perm("articles.change_article"):
                # hasn't permission to change
                raise PermissionDenied

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
                if a.draft:
                    return redirect(articles_by_user)
                else:
                    message = "Din artikel är nu skickad för granskning."
                    return render(request, "articles/confirmation.html", {'message': message})

        else:
            form = ArticleForm(instance=a)
            return render(request, 'articles/article_form.html', {'form': form})
    else:
        # Error not logged in
        raise PermissionDenied



def single_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    if article.approved:
        return render(request, 'articles/article.html', {'article': article})
    elif request.user == article.user:
        return render(request,'articles/article.html', {'article': article})
    raise PermissionDenied


def all_articles(request):
    articles = Article.objects.filter(approved=True)
    return render(request, 'articles/articles.html', {'articles': articles})

@login_required()
def all_unapproved_articles(request):
    if request.user.has_perm("articles.can_approve_article"):
        articles = Article.objects.filter(approved=False, draft=False)
        return render(request, 'articles/approve_articles.html', {'articles': articles})
    else:
        raise PermissionDenied

@login_required()
def approve_article(request, article_id):
    if request.user.has_perm("articles.can_approve_article"):
        a = Article.objects.get(pk=article_id)
        if a.draft:
            # cant publish article in draft state
            return HttpResponseForbidden()
        a.approved = True
        a.save()
        return redirect(all_unapproved_articles)
    else:
        raise PermissionDenied

@login_required()
def unapprove_article(request, article_id):
    if request.user.has_perm("articles.can_approve_article"):
        a = Article.objects.get(pk=article_id)
        a.draft = True
        a.save()
        message = "Artikeln har gått tillbaka till draft läget, maila gärna " + a.user.email + " med en förklaring."
        return render(request, 'articles/confirmation.html', {'message': message})
    else:
        raise PermissionDenied


def articles_by_tag(request, tag_name):
    articles = Tag.objects.get(name=tag_name).article_set.filter(approved=True)
    return render(request, 'articles/articles.html', {'articles': articles})


@login_required()
def articles_by_user(request):
    approved_articles = request.user.article_set.filter(approved=True)
    unapproved_articles = request.user.article_set.filter(approved=False, draft=False)
    draft_articles = request.user.article_set.filter(draft=True)

    return render(request, 'articles/my_articles.html', {'approved_articles': approved_articles,
                                                         'unapproved_articles': unapproved_articles,
                                                         'draft_articles': draft_articles})
