from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.forms import modelformset_factory
from .models import Organisation, OrganisationPost
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
def edit_memebers(request, organisation_name):
    my_organisation = Organisation.objects.get(name=organisation_name)

    # Only the leader can change a organization.
    if not my_organisation.can_edit(request.user):
        return HttpResponseForbidden()

    OrgPostFormSet = modelformset_factory(OrganisationPost,
                                          fields=('post', 'user', 'email'),
                                          max_num=100,
                                          extra=5,
                                          can_delete=True)

    if request.method == 'POST':
        formset = OrgPostFormSet(request.POST)
        if formset.is_valid():
            group = my_organisation.group
            for entry in formset.cleaned_data:
                if entry['DELETE']:
                    group.user_set.remove(entry.user)  # Delete
                    org_post.objects.get(pk=entry['id'])
                    org_post.delete()
                else:
                    if entry['id']:
                        org_post = OrganisationPost.objects.get(pk=entry['id'])  # Update
                    else:
                        org_post = OrganisationPost(org=my_organisation)  # Create
                    org_post.email = entry['email']
                    org_post.post = entry['post']
                    org_post.user = entry['user']
                    org_post.save()
            return redirect("edit_organisation_members")
        else:
            return render(request, "organisations/members.html", {
                        'organisation': my_organisation,
                        'formset': formset,
                        })

    orgPosts = OrganisationPost.objects.filter(org=my_organisation)
    formset = OrgPostFormSet(queryset=orgPosts)
    return render(request, "organisations/members.html", {
                        'organisation': my_organisation,
                        'formset': formset,
                        })


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
