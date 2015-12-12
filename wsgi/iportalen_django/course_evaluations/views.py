from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils import timezone
from course_evaluations.forms import EvaluationForm
from .models import Period, Course, Evaluation, Reward

def evaluate_course(request):
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

    return render(request, "course_evaluations/evaluate_course.html", {"form": form, "rewards": rewards, "period": p, "user_evaluations": user_eval})
