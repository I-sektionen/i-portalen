from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction
from .models import Article, Tag
from .forms import ArticleForm


@login_required()
@transaction.atomic
def create_or_modify_article(request, article_id=None):
    a = None
    if article_id:
        a = Article.objects.get(pk=article_id)
        if (a.user != request.user or not request.user.has_perm("articles.change_article")) \
                and not request.user.has_perm("articles.can_approve_article"):
            # hasn't permission to change
            raise PermissionDenied
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=a)

        # check whether it's valid:
        if form.is_valid(user=request.user):
            a = form.save(commit=False)
            if a.approved:
                a.replacing_id = a.id
                a.approved = False
                a.id = None

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
                return render(request, "articles/confirmation.html", {'message': message, 'article_id': article_id})
        else:
            return render(request, 'articles/article_form.html', {'form': form, 'article_id': article_id})
    else:
        form = ArticleForm(instance=a)
        return render(request, 'articles/article_form.html', {'form': form, 'article_id': article_id})


def single_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    if article.approved:
        return render(request, 'articles/article.html', {'article': article})
    elif request.user == article.user:
        return render(request, 'articles/article.html', {'article': article})
    raise PermissionDenied


def all_articles(request):
    articles = Article.objects.filter(approved=True,
                                      visible_from__lte=timezone.now(),
                                      visible_to__gte=timezone.now())
    return render(request, 'articles/articles.html', {'articles': articles})


@login_required()
def all_unapproved_articles(request):
    if request.user.has_perm("articles.can_approve_article"):
        articles = Article.objects.filter(approved=False, draft=False, visible_to__gte=timezone.now())
        return render(request, 'articles/approve_articles.html', {'articles': articles})
    else:
        raise PermissionDenied


@login_required()
@transaction.atomic
def approve_article(request, article_id):
    if request.user.has_perm("articles.can_approve_article"):
        a = Article.objects.get(pk=article_id)
        if a.draft:
            # cant publish article in draft state
            return HttpResponseForbidden()
        a.approved = True
        a.save()
        if a.replacing:
            old = Article.objects.get(pk=a.replacing_id)
            old.delete()
            a.pk = a.replacing_id
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
        message = ("Artikeln har gått tillbaka till utkast läget, maila gärna <a href='mailto:" +
                   a.user.email +
                   "?Subject=Avslag%20publicering%20av%20artikel' target='_top'>" +
                   a.user.email +
                   "</a> med en förklaring till avslaget.<br>" +
                   "<a href='/articles/unapproved'>Tillbaka till listan över artiklar att godkänna.</a>")
        return render(request, 'articles/confirmation.html', {'message': message})
    else:
        raise PermissionDenied


def articles_by_tag(request, tag_name):
    articles = Tag.objects.get(name=tag_name).article_set.filter(approved=True)
    return render(request, 'articles/articles.html', {'articles': articles})


@login_required()
def articles_by_user(request):
    user_articles = request.user.article_set.filter(visible_to__gte=timezone.now()).order_by('-created')
    return render(request, 'articles/my_articles.html', {'user_articles': user_articles})

@login_required()
def delete_article(request, article_id):
    article = Article.objects.get(pk=article_id)

    if article.draft and request.user == article.user:
        article.delete()
        return redirect(articles_by_user)
    raise PermissionDenied

@login_required()
def article_file_download(request, article_id):
    article = Article.objects.get(pk=article_id)
    article_filename = article.attachment
    response = HttpResponse(article_filename)
    response['Content-Disposition'] = 'attachment; filename="article_file.pdf"'

    return response
