from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from articles.models import Article
from events.models import Event


def placeholder(request):
    return render(request, "placeholder.html")


@login_required()
def glasscubes_link(request):
    return redirect("https://industriellekonomi.glasscubes.com/share/s/d6msv3iv5a4g36o8d5q1ct2uvm")


def isektionen_link(request):
    return redirect("https://www.isektionen.se/")


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


def display_sponsored_content(request):
    content_feed_list = list(Article.objects.filter(
        status=Article.APPROVED,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now(),
        sponsored=True
    ).order_by('-visible_from'))
    content_feed_list += list(Event.objects.filter(
        status=Event.APPROVED,
        visible_from__lte=timezone.now(),
        end__gte=timezone.now(),
        sponsored=True
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

    return render(request, 'sponsored.html', {'content_feed_list': content})
