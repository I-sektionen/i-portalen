from django.core.exceptions import PermissionDenied
from django.shortcuts import render

# Create your views here.
from fika_penalty.models import FikaPenalty
from organisations.models import Organisation


def all_penalties(request):
    all_p = FikaPenalty.objects.all()
    return render(request, "fika_penalty/all_penalties.html", {"penalties": all_p})


def penalties_per_organisation(request, organisation_name):
    if Organisation.objects.get(name=organisation_name).user_in_organisation(request.user):
        p = FikaPenalty.objects.filter(organisation__name=organisation_name)
        return render(request, "fika_penalty/all_penalties.html", {"penalties": p})
    raise PermissionDenied
