from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.forms import modelformset_factory, formset_factory
from django.shortcuts import render, redirect
from django.utils import timezone
from course_evaluations.forms import EvaluationForm, PeriodForm, YearForm, CourseForm
from .models import Period, Course, Evaluation, Reward, Year, CourseEvaluationSettings
from utils.markdown import markdown_to_html
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _

@login_required
def evaluate_course(request):
    setting = CourseEvaluationSettings.objects.all()
    if setting.exists():
        settings = setting[0]
    else:
        settings = None
    try:
        p = Period.objects.get(start_date__lte=timezone.now(), end_date__gte=timezone.now())
    except Period.DoesNotExist:
        messages.error(request, _("Ingen anmälan till kursutvärderingar är öppen!"))
        return render(request, "course_evaluations/evaluate_course.html", {"form": None})
    except Period.MultipleObjectsReturned:
        messages.error(request, _("Flera utvärderingsperioder är aktiva samtidigt!"))
        return render(request, "course_evaluations/evaluate_course.html", {"form": None})

    rewards = Reward.objects.all()
    form = EvaluationForm(request.POST or None, period=p)
    user_eval = Evaluation.objects.filter(period=p, user=request.user)
    if request.POST:
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.user = request.user
            evaluation.period = p
            try:
                evaluation.full_clean()
            except ValidationError:
                messages.error(request, _("Valideringsfel! Detta beror förmodligen på att kursen "
                                          "du valt är redan har blivit tagen för utvärdering."))
                form = EvaluationForm(None, period=p)
                return render(request, "course_evaluations/evaluate_course.html", {"form": form})
            evaluation.save()
            subject = _("Viktig information till dig som är utvärderingsansvarig!!")
            body = markdown_to_html(settings.mail_to_evaluator).format(
                user=request.user.first_name.capitalize(),
                period=p.name,
                year=p.get_year,
                course=evaluation.course)
            subject_org = _("Viktig information till dig som är utvärderingsansvarig!!")
            body_org = markdown_to_html(settings.mail_to_organisation).format(
                user=request.user.get_full_name,
                user_email=request.user.email,
                period=p.name,
                year=p.get_year,
                course=evaluation.course,
                reward=evaluation.reward)
            email_list = []
            for email in settings.mail_addresses_to_organisation.split():
                email_list.append(email)
            send_mail(subject, "", django_settings.EMAIL_HOST_USER, [request.user.email, ], fail_silently=False, html_message=body)
            send_mail(subject_org, "", django_settings.EMAIL_HOST_USER, email_list, fail_silently=False, html_message=body_org)
            form = EvaluationForm(None, period=p)
    return render(request, "course_evaluations/evaluate_course.html", {
        "form": form, "rewards": rewards, "period": p, "user_evaluations": user_eval, "settings": settings})


@login_required
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def admin(request):
    return render(request, "course_evaluations/admin/index.html",)


@login_required
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def admin_year(request, year):
    year = Year.objects.get(year=year)
    courses = Course.objects.all()
    if request.method == 'POST':
        year.vt1.update_courses_from_list(request.POST.getlist('courses_vt1'))
        year.vt2.update_courses_from_list(request.POST.getlist('courses_vt2'))
        year.ht1.update_courses_from_list(request.POST.getlist('courses_ht1'))
        year.ht2.update_courses_from_list(request.POST.getlist('courses_ht2'))

    return render(request, "course_evaluations/admin/year.html", {"year": year, "courses": courses})


@login_required
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def create_or_modify_rewards(request):
    rewards = Reward.objects.all()
    RewardFormSet = modelformset_factory(Reward, fields="__all__", max_num=1000, extra=5, can_delete=False)

    if request.method == 'POST':
        formset = RewardFormSet(request.POST)
        if formset.is_valid():
            for entry in formset.cleaned_data:
                if not entry == {}:
                    if entry['id']:
                        entry['id'].active = entry["active"]
                        entry['id'].save()
                    else:
                        Reward.objects.create(name=entry['name'], active=entry['active'])
            formset = RewardFormSet()
            return render(request, "course_evaluations/admin/add_rewards.html", {"formset": formset, "rewards": rewards})
        else:
            return render(request, "course_evaluations/admin/add_rewards.html", {"formset": formset, "rewards": rewards})

    formset = RewardFormSet()
    return render(request, "course_evaluations/admin/add_rewards.html", {"formset": formset, "rewards": rewards})


@login_required
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def choose_year(request):
    years = Year.objects.all()
    return render(request, "course_evaluations/admin/choose_year.html", {"years": years})


@login_required
@transaction.atomic
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def copy_last_year(request):
    year = Year.objects.copy_last_year()
    year.save()
    return redirect(year)


@login_required
@transaction.atomic
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def create_year(request):
    form = YearForm(request.POST or None)
    if request.POST:
        if form.is_valid():

            try:
                ht1 = Period(start_date=form.cleaned_data['ht1_start'],
                             end_date=form.cleaned_data['ht2_start']-timezone.timedelta(days=1),
                             name="HT1")

                ht2 = Period(start_date=form.cleaned_data['ht2_start'],
                             end_date=form.cleaned_data['ht2_end'],
                             name="HT2")

                vt2 = Period(start_date=form.cleaned_data['vt2_start'],
                             end_date=form.cleaned_data['vt2_end'],
                             name="VT2")
                vt1 = Period(start_date=form.cleaned_data['vt1_start'],
                             end_date=form.cleaned_data['vt2_start']-timezone.timedelta(days=1),
                             name="VT1")
                vt1.clean()
                vt2.clean()
                ht1.clean()
                ht2.clean()
            except ValidationError:
                form.add_error('vt1_start', _("VT1 överlappar med föregående år! var vänlig sätt ett annat datum!"))
                return render(request, "course_evaluations/admin/create_year.html", {"form": form})
            vt1.save()
            vt2.save()
            ht1.save()
            ht2.save()

            year = Year(year=form.cleaned_data['year'],
                        vt1=vt1,
                        vt2=vt2,
                        ht1=ht1,
                        ht2=ht2)
            year.save()
            return redirect(year)
    return render(request, "course_evaluations/admin/create_year.html", {"form": form})


@login_required
@transaction.atomic
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def admin_period(request, pk):
    period = Period.objects.get(pk=pk)
    return render(request, "course_evaluations/admin/period.html", {"period": period})


@login_required
@transaction.atomic
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def edit_period(request, pk):
    period = Period.objects.get(pk=pk)
    form = PeriodForm(request.POST or None, instance=period)
    if request.POST:
        if form.is_valid():
            form.save()

    return render(request, "course_evaluations/admin/edit_period.html", {'period': period, "form": form})


@login_required
@transaction.atomic
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def evaluations(request, pk):
    period = Period.objects.get(pk=pk)
    if request.POST:
        remove = request.POST.getlist('remove')
        evaluated = request.POST.getlist('evaluated')
        for r in remove:
            period.evaluation_set.get(pk=r).delete()
        for e in period.evaluation_set.all():
            if str(e.pk) in evaluated:
                e.evaluated = True
                e.save()
            else:
                e.evaluated = False
                e.save()

    return render(request, "course_evaluations/admin/evaluations.html", {"period": period})


@login_required
@transaction.atomic
@permission_required('course_evaluations.add_course')
@permission_required('course_evaluations.change_course')
@permission_required('course_evaluations.delete_course')
def create_courses(request):
    courses = Course.objects.all()
    CourseFormSet = formset_factory(CourseForm, max_num=1000, extra=10, can_delete=False)

    if request.method == 'POST':
        formset = CourseFormSet(request.POST)
        if formset.is_valid():
            for entry in formset.cleaned_data:
                if not entry == {}:
                    Course.objects.create(code=entry['code'], name=entry['name'])
            formset = CourseFormSet()
            return render(request, "course_evaluations/admin/add_courses.html", {"formset": formset, "courses": courses})
        else:
            return render(request, "course_evaluations/admin/add_courses.html", {"formset": formset, "courses": courses})

    formset = CourseFormSet()
    return render(request, "course_evaluations/admin/add_courses.html", {"formset": formset, "courses": courses})
