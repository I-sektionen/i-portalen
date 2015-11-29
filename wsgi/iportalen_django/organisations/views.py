from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Organisation
from .forms import OrganisationForm, AddOrganisationForm


def organisation(request, organisation_name):
    return render(request, "organisations/organisation.html",
                  {'organisation': get_object_or_404(Organisation, name=organisation_name)})


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
        return render(request, "organisations/organisation_form.html",
                      {'organisation': Organisation.objects.get(name=organisation_name), "form": form})


@login_required()
def add_organisation(request):
    if not request.user.has_perm('organisations.add_organisation'):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = AddOrganisationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Organisationen: {:} har skapats".format(form.cleaned_data['name']))
            form = AddOrganisationForm()
    else:
        form = AddOrganisationForm()
    return render(request, "organisations/add_org_form.html", {"form": form})
