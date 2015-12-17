from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import modelformset_factory, formset_factory
from django.shortcuts import render, redirect
from django.utils import timezone
from course_evaluations.forms import EvaluationForm, PeriodForm, YearForm, CourseForm, RewardForm
from .models import Period, Course, Evaluation, Reward, Year, CourseEvaluationSettings


@login_required
def evaluate_course(request):
    settings = CourseEvaluationSettings.objects.all()
    if settings.exists():
        settings = settings[0]
    else:
        settings = None
    try:
        p = Period.objects.get(start_date__lte=timezone.now(), end_date__gte=timezone.now())
    except Period.DoesNotExist:
        messages.error(request, "Ingen anmälan till kursutvärderingar är öppen!")
        return render(request, "course_evaluations/evaluate_course.html", {"form": None})
    except Period.MultipleObjectsReturned:
        messages.error(request, "Flera utvärderingsperioder är aktiva samtidigt!")
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
                messages.error(request, "Valideringsfel! Detta beror förmodligen på att kursen du valt är redan har blivit tagen för utvärdering.")
                form = EvaluationForm(None, period=p)
                return render(request, "course_evaluations/evaluate_course.html", {"form": form})
            evaluation.save()
            form = EvaluationForm(None, period=p)
    leader = "Lovisa Annerwall"  # TODO: get this from organisation
    return render(request, "course_evaluations/evaluate_course.html", {
        "form": form, "rewards": rewards, "period": p, "user_evaluations": user_eval, "settings": settings})


@login_required
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
def admin(request):
    return render(request, "course_evaluations/admin/index.html",)


@login_required
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
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
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
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
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
def choose_year(request):
    years = Year.objects.all()
    return render(request, "course_evaluations/admin/choose_year.html", {"years": years})


@login_required
@transaction.atomic
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
def copy_last_year(request):
    year = Year.objects.copy_last_year()
    year.save()
    return redirect(year)


@login_required
@transaction.atomic
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
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
                form.add_error('vt1_start', 'VT1 överlappar med föregående år! var vänlig sätt ett annat datum!')
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
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
def admin_period(request, pk):
    period = Period.objects.get(pk=pk)
    return render(request, "course_evaluations/admin/period.html", {"period": period})


@login_required
@transaction.atomic
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
def edit_period(request, pk):
    period = Period.objects.get(pk=pk)
    form = PeriodForm(request.POST or None, instance=period)
    if request.POST:
        if form.is_valid():
            form.save()

    return render(request, "course_evaluations/admin/edit_period.html", {'period': period, "form": form})


def evaluations(request, pk):
    period = Period.objects.get(pk=pk)
    return render(request, "course_evaluations/admin/evaluations.html", {"period": period})

@login_required
@transaction.atomic
@permission_required('courses.add_course')
@permission_required('courses.change_course')
@permission_required('courses.delete_course')
def create_courses(request):
    courses = Course.objects.all()
    CourseFormSet = formset_factory(CourseForm, max_num=1000, extra=10, can_delete=False)

    if request.method == 'POST':
        formset = CourseFormSet(request.POST)
        if formset.is_valid():
            for entry in formset.cleaned_data:
                if not entry == {}:
                    c = Course.objects.create(code=entry['code'], name=entry['name'])
                    print(c)
            formset = CourseFormSet()
            return render(request, "course_evaluations/admin/add_courses.html", {"formset": formset, "courses": courses})
        else:
            return render(request, "course_evaluations/admin/add_courses.html", {"formset": formset, "courses": courses})

    formset = CourseFormSet()
    return render(request, "course_evaluations/admin/add_courses.html", {"formset": formset, "courses": courses})
