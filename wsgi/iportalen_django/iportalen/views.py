from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from articles.models import Article
from events.models import Event


@login_required()
def create_content(request):
    return render(request, "iportalen/create_content.html")


@login_required()
def approve_content(request):
    return render(request, "iportalen/approve_content.html")


def placeholder(request):
    return render(request, "placeholder.html")


def article_pagination(request):
    article_list = Article.objects.filter(
        status=Article.APPROVED,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now()
    ).order_by('-visible_from')

    paginator = Paginator(article_list, 14)

    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'front_page.html', {'articles': articles})


def display_news_feed(request):
    content_feed_list = list(Article.objects.filter(
        status=Article.APPROVED,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now()
    ).order_by('-visible_from'))
    content_feed_list += list(Event.objects.filter(
        status=Event.APPROVED,
        visible_from__lte=timezone.now(),
        end__gte=timezone.now()
    ).order_by('-visible_from'))

    content_feed_list = sorted(content_feed_list, key=lambda contents: contents.visible_from, reverse=True)
    paginator = Paginator(content_feed_list, 14)

    page = request.GET.get('page')

    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    return render(request, 'landing.html', {'content_feed_list': content})
