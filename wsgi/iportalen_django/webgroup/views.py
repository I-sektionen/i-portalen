from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from utils.liu_student import MultipleMatches
from .models import Course, Groupings


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
        min_participants = int(request.GET.get('min_participants', 0))
    except ValueError:
        min_participants = 0
    try:
        [date_from, date_to] = date_range.split(" - ")
    except AttributeError:
        date_from = None
        date_to = None
    url_filter = {
        "course": course,
        "exam": exam,
        "date_from": date_from,
        "date_to": date_to,
        "min_participants": min_participants
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
            data = tmp.google_chart(exam, date_from, date_to, min_participants)
            return render(request, "webgroup/exam_statistics.html", {"result": tmp, "filter": url_filter, "google_chart": data['json']})
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


@login_required
def exam_statistics_groups(request):
    group = request.GET.get('group')
    date_range = request.GET.get('daterange')
    try:
        min_participants = int(request.GET.get('min_participants', 0))
    except ValueError:
        min_participants = 0
    try:
        [date_from, date_to] = date_range.split(" - ")
    except AttributeError:
        date_from = None
        date_to = None
    url_filter = {
        "group": group,
        "date_from": date_from,
        "date_to": date_to,
        "min_participants": min_participants
    }
    courses = []
    try:
        g = Groupings.objects.get(pk=group)
        course_objects = g.courses.all()
        for c in course_objects:
            tmp = c.statistics(date_from, date_to, min_participants)
            for k, v in list(tmp.items()):
                if tmp[k]['summed'] == 0:
                    del tmp[k]
                    continue
                try:
                    tmp[k]["kugg"] = round(tmp[k]["U"]*1000/tmp[k]["summed"])/10
                except (KeyError, ZeroDivisionError):
                    tmp[k]["kugg"] = 0
                try:
                    tmp[k]["3or"] = round(tmp[k]["3"] * 1000 / tmp[k]["summed"]) / 10
                except (KeyError, ZeroDivisionError):
                    tmp[k]["3or"] = 0
                try:
                    tmp[k]["4or"] = round(tmp[k]["4"] * 1000 / tmp[k]["summed"]) / 10
                except (KeyError, ZeroDivisionError):
                    tmp[k]["4or"] = 0
                try:
                    tmp[k]["5or"] = round(tmp[k]["5"] * 1000 / tmp[k]["summed"]) / 10
                except (KeyError, ZeroDivisionError):
                    tmp[k]["5or"] = 0
                try:
                    tmp[k]["pass"] = round(tmp[k]["G"] * 1000 / tmp[k]["summed"]) / 10
                except (KeyError, ZeroDivisionError):
                    tmp[k]["pass"] = 0

            tmp["course_code"] = c.course_code
            tmp["course_name"] = c.name
            courses.append(tmp)
    except Groupings.DoesNotExist:
        pass
    return render(request, "webgroup/exam_statistics_groups.html", {"result": None, "filter": url_filter, "groups": Groupings.objects.all(), "courses": courses})
