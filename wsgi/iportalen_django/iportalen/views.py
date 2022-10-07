from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from user_managements.forms import ChangeUserInfoForm
from articles.models import Article
from events.models import Event


def placeholder(request):
    return render(request, "placeholder.html")


@login_required()
def glasscubes_link(request):
    return redirect("https://drive.google.com/drive/folders/1OlboXaiTWsYiYxcYJK8p3KSX7x9F6QBZ?usp=sharing")


@login_required()
def glasscubes_link_course(request):
    return redirect("https://drive.google.com/drive/folders/1LVqroOU6AUtJTIGGFU1aZPtKH0JSjmlJ?usp=sharing")


@login_required()
def glasscubes_link_bible(request):
    return redirect("https://drive.google.com/drive/folders/14YmOgL9-5x8ca8VZOKaji4MXiLyAtUyP?usp=sharing")


def isektionen_link(request):
    return redirect("https://www.isektionen.se/")


def landing(request):
    if request.user is not None:
        if request.user.is_active and request.user.is_member is True:
            if request.user.must_edit or request.user.date_gdpr_accepted is None:
                form = ChangeUserInfoForm(instance=request.user)
                return render(request, "user_managements/force_user_form.html", {"form": form})
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


def display_job_advert_content(request):
    content_feed_list = list(Article.objects.filter(
        status=Article.APPROVED,
        visible_from__lte=timezone.now(),
        visible_to__gte=timezone.now(),
        job_advert=True
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

    return render(request, 'job_adverts.html', {'content_feed_list': content})
