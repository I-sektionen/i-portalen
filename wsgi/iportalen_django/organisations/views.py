from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Organisation
from .forms import OrganisationForm

# Create your views here.
def all_organisations(request):
    return render(request, "organisations/organisations.html", {'organisations': Organisation.objects.all()})

def organisation(request, organisation_name):
    return render(request, "organisations/organisation.html", {'organisation': Organisation.objects.get(name=organisation_name)})

@login_required()
def edit_organisation(request, organisation_name):
    my_organisation = Organisation.objects.get(name=organisation_name)

    # Only the leader can change a organization.
    if not my_organisation.can_edit(request.user):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = OrganisationForm(request.POST, request.FILES, instance=my_organisation)

        if form.is_valid():
            form.save()

        return redirect(reverse("organisation", kwargs={'organisation_name': organisation_name}))
    else:
        form = OrganisationForm(instance=my_organisation)
        return render(request, "organisations/organisation_form.html", {'organisation': Organisation.objects.get(name=organisation_name), "form": form})
