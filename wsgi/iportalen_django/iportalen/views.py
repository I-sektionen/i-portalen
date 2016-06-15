from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from articles.models import Article
from events.models import Event


def placeholder(request):
    return render(request, "placeholder.html")


@login_required()
def glasscubes_link(request):
    return redirect("https://www.dropbox.com/sh/ah2wws4hsu1p184/AAAhfa1l-AvbBGzKPNS3AYQUa?dl=0")


@login_required()
def glasscubes_link_course(request):
    return redirect("https://www.dropbox.com/sh/8n3t8om0rkqlkem/AAA0igQbQB_C7q4LLbGwUKPaa?dl=0")


@login_required()
def glasscubes_link_bible(request):
    return redirect("https://www.dropbox.com/sh/rd3rcmfepq036uq/AABtg4JSpCxWVmLjJ2NGM0L0a?dl=0")


def isektionen_link(request):
    return redirect("https://www.isektionen.se/")


def landing(request):
    return render(request, 'landing.html')


@csrf_exempt
def news_content(request):
    if request.method == "POST":
        tags = request.POST.getlist('tags[]')
        if int(request.POST.get('articles')) == 1:
            articles = Article.objects.published()
        else:
            articles = Article.objects.none()

        if int(request.POST.get('events')) == 1:
            events = Event.objects.published()
        else:
            events = Event.objects.none()

        if int(request.POST.get('sponsored')) == 1:
            articles = articles.filter(sponsored=True)
            events = events.filter(sponsored=True)

        if tags:
            articles = articles.filter(tags__in=tags)
            events = events.filter(tags__in=tags)
        content_feed_list = list(articles.distinct().order_by('-visible_from'))
        content_feed_list += list(events.distinct().order_by('-visible_from'))

        content_feed_list = sorted(content_feed_list, key=lambda contents: contents.visible_from, reverse=True)
        paginator = Paginator(content_feed_list, 20)

        page = request.GET.get('page')

        try:
            content = paginator.page(page)
        except PageNotAnInteger:
            content = paginator.page(1)
        except EmptyPage:
            content = paginator.page(paginator.num_pages)

        html = render_to_string('news_content.html', {'content_feed_list': content})
        return HttpResponse(html)
    raise Http404


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
