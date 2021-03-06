from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.forms import modelformset_factory
from .models import Organisation, OrganisationPost
from .forms import OrganisationForm, AddOrganisationForm
from django.utils.translation import ugettext as _


def organisation(request, organisation_name):
    org = get_object_or_404(Organisation, name=organisation_name)
    members = OrganisationPost.objects.filter(org=org)
    return render(request, "organisations/organisation.html", {
        'organisation': org,
        'members': members
    })


@login_required()
@transaction.atomic
def edit_organisation(request, organisation_name):
    my_organisation = Organisation.objects.get(name=organisation_name)

    # Only the leader can change a organization.
    if not my_organisation.can_edit(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = OrganisationForm(request.POST, request.FILES, instance=my_organisation)

        if form.is_valid():
            org=form.save()
            org.modified_by=request.user
            org.save()

        return redirect(reverse("organisations:organisation", kwargs={'organisation_name': organisation_name}))
    else:
        form = OrganisationForm(instance=my_organisation)
        return render(request, "organisations/organisation_form.html",
                      {'organisation': Organisation.objects.get(name=organisation_name), "form": form})


@login_required()
@transaction.atomic
def edit_memebers(request, organisation_name):
    my_organisation = Organisation.objects.get(name=organisation_name)

    # Only the leader can change a organization.
    if not my_organisation.can_edit(request.user):
        raise PermissionDenied

    OrgPostFormSet = modelformset_factory(OrganisationPost,
                                          fields=('post', 'user', 'email'),
                                          max_num=100,
                                          extra=5,
                                          can_delete=True)

    if request.method == 'POST':
        formset = OrgPostFormSet(request.POST, queryset=OrganisationPost.objects.filter(org=my_organisation))
        if formset.is_valid():
            group = my_organisation.group
            for entry in formset.cleaned_data:
                if not entry == {}:
                    if entry['DELETE']:
                        try:
                            group.user_set.remove(entry.user)  # Delete
                        except AttributeError:  # No groups for user.
                            pass
                        entry['id'].delete()
                    else:
                        if entry['id']:
                            org_post = entry['id']  # Update
                        else:
                            org_post = OrganisationPost(org=my_organisation)  # Create
                        org_post.email = entry['email']
                        org_post.post = entry['post']
                        org_post.user = entry['user']
                        org_post.modified_by=request.user
                        org_post.save()
                        group.user_set.add(org_post.user)
            return redirect("organisations:edit organisation members", organisation_name=my_organisation.name)
        else:
            return render(request, "organisations/members.html", {
                        'organisation': my_organisation,
                        'formset': formset,
                        })

    formset = OrgPostFormSet(queryset=OrganisationPost.objects.filter(org=my_organisation))
    return render(request, "organisations/members.html", {
                        'organisation': my_organisation,
                        'formset': formset,
                        })


@login_required()
@transaction.atomic
def add_organisation(request):
    if not request.user.has_perm('organisations.add organisation'):
        raise PermissionDenied
    if request.method == 'POST':
        form = AddOrganisationForm(request.POST)
        if form.is_valid():
            org = form.save()
            org.modified_by=request.user
            org.save()
            messages.info(request, "".join([_("Organisationen:"), " {:} ", _("har skapats")]).format(
                form.cleaned_data['name']))
            form = AddOrganisationForm()
    else:
        form = AddOrganisationForm()
    return render(request, "organisations/add_org_form.html", {"form": form})
