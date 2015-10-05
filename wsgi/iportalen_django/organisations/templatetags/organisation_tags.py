from django.db.models import Q

__author__ = 'jonathan'
from django.template.loader_tags import register
from organisations.models import Organisation

@register.assignment_tag
def get_all_organisations():
    organisations = Organisation.objects.all().order_by('-name')
    return organisations

@register.assignment_tag
def get_organisation(pk):
    organisation = Organisation.objects.get(pk=pk)
    return organisation

@register.assignment_tag
def get_menu_organisations():
    organisations = {
        "sektionen": list(Organisation.objects.filter(
            organisation_type=Organisation.SEKTIONEN,
            parent_organisation=None
        ).order_by('name')),
        "utskott": list(Organisation.objects.filter(
            organisation_type=Organisation.UTSKOTT,
            parent_organisation=None
        ).order_by('name')),
        "foreningar": list(Organisation.objects.filter(
            organisation_type=Organisation.FORENINGAR,
            parent_organisation=None
        ).order_by('name')),
    }
    sektionen_children = Organisation.objects.filter(
            ~Q(parent_organisation=None), organisation_type=Organisation.SEKTIONEN,
        ).order_by('name')
    for u in sektionen_children:
        for p in organisations["sektionen"]:
            if p.name == u.parent_organisation.name:
                if hasattr(p, "children_organisations"):
                    p.children_organisations.append(u)
                else:
                    p.children_organisations = [u]
    utskott_children = Organisation.objects.filter(
            ~Q(parent_organisation=None), organisation_type=Organisation.UTSKOTT,
        ).order_by('name')
    for u in utskott_children:
        for p in organisations["utskott"]:
            if p.name == u.parent_organisation.name:
                if hasattr(p, "children_organisations"):
                    p.children_organisations.append(u)
                else:
                    p.children_organisations = [u]
    foreningar_children = Organisation.objects.filter(
            ~Q(parent_organisation=None), organisation_type=Organisation.FORENINGAR,
        ).order_by('name')
    for u in foreningar_children:
        for p in organisations["foreningar"]:
            if p.name == u.parent_organisation.name:
                if hasattr(p, "children_organisations"):
                    p.children_organisations.append(u)
                else:
                    p.children_organisations = [u]

    return organisations