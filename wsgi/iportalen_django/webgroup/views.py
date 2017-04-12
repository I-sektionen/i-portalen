from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from utils.liu_student import MultipleMatches
from .models import Course


def landing(request):
    return render(request, "webgroup/landing.html", {})


def github_stats(request):
    return render(request, "webgroup/github.html", {})


@login_required
def exam_statistics(request):
    course = request.GET.get('course')
    exam = request.GET.get('exam')
    date_range = request.GET.get('daterange')
    try:
        [date_from, date_to] = date_range.split(" - ")
    except AttributeError:
        date_from = None
        date_to = None
    url_filter = {
        "course": course,
        "exam": exam,
        "date_from": date_from,
        "date_to": date_to
    }
    try:
        if len(course) >= 6:
            try:
                tmp = Course.objects.get(course_code=course.upper())
            except Course.DoesNotExist:
                tmp = Course()
                tmp.course_code = course.upper()
                try:
                    res = tmp.collect_results()
                except MultipleMatches:
                    messages.error(request, "Kurskoden gav inte en unik träff i sökningen.")
                    return render(request, "webgroup/exam_statistics.html", {"result": None, "filter": url_filter})
                if res:
                    tmp.name = res[0]["course_name"]
                    tmp.save()
                    tmp.store_results(res)
                else:
                    messages.error(request, "Sökningen gav ingen träff.")
                    return render(request, "webgroup/exam_statistics.html", {"result": None, "filter": url_filter})
            return render(request, "webgroup/exam_statistics.html", {"result": tmp, "filter": url_filter, "google_chart": tmp.google_chart(exam, date_from, date_to)})
        else:
            messages.error(request, "Kurskoden gav inte en unik träff i sökningen.")
    except TypeError:
        pass
    return render(request, "webgroup/exam_statistics.html", {"result": None, "filter": url_filter})


@login_required
def exam_statistics_update(request):
    course = request.GET.get('course')
    if len(course) >= 6:
        try:
            tmp = Course.objects.get(course_code=course.upper())
            tmp.collect_and_store_results()
            return redirect(reverse("webgroup:exam_statistics") + "?course={}".format(course))
        except Course.DoesNotExist:
            messages.error(request, "Kurskoden gav inte någon träff.")
    else:
        messages.error(request, "Kurskoden gav inte en unik träff i sökningen.")
    return redirect(reverse("webgroup:exam_statistics")+"?course={}".format(course))
