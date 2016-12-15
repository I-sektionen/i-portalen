from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from rest_framework.reverse import reverse

from fika_penalty.forms import FikaPenaltyForm
from fika_penalty.models import FikaPenalty
from organisations.models import Organisation


def all_penalties(request):
    all_p = FikaPenalty.objects.all()
    return render(request, "fika_penalty/all_penalties.html", {"penalties": all_p})


def history_penalties_per_organisation(request, organisation_name):
    organisation = Organisation.objects.get(name=organisation_name)
    if organisation.user_in_organisation(request.user):
        p = FikaPenalty.objects.filter(organisation__name=organisation_name).order_by("date")
        return render(request, "fika_penalty/all_penalties.html", {"penalties": p, 'sum': FikaPenalty.objects.get_sum_per_organisation(organisation), "organisation": organisation})
    raise PermissionDenied


def add_penalty_per_organisation(request, organisation_name):
    organisation = Organisation.objects.get(name=organisation_name)
    if organisation.leader == request.user:
        form = FikaPenaltyForm(request.POST or None, organisation=organisation)
        if request.method == "POST":
            if form.is_valid():
                fika = form.save(commit=False)
                fika.organisation = organisation
                fika.date = timezone.now()
                fika.save()
                form = FikaPenaltyForm(None, organisation=organisation)
                messages.success(request, "Kostnaden är bokförd!")
                return redirect(reverse('fika_penalty:organisation penalties', args=[organisation_name]))
        return render(request, "fika_penalty/penalty_form.html", {"form": form, "organisation": organisation})
    raise PermissionDenied


def penalties_per_organisation(request, organisation_name):
    organisation = Organisation.objects.get(name=organisation_name)
    if organisation.user_in_organisation(request.user):
        p = FikaPenalty.objects.filter(organisation__name=organisation_name).values('user').annotate(sum=Sum('cost'))
        return render(request, "fika_penalty/penalties.html", {"penalties": p, 'sum': FikaPenalty.objects.get_sum_per_organisation(organisation), "organisation": organisation})
    raise PermissionDenied
