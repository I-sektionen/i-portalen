from django.core.urlresolvers import reverse
from django.template.loader_tags import register
from organisations.models import Organisation
from django.utils.translation import ugettext as _


@register.assignment_tag
def get_menu_organisations():
    organisations = {
        "sektionen": list(Organisation.objects.filter(
            organisation_type=Organisation.SEKTIONEN,
        ).order_by('name')),
        "foreningar": list(Organisation.objects.filter(
            organisation_type=Organisation.FORENINGAR,
        ).order_by('name')),
    }
    return organisations


@register.assignment_tag
def get_child_organisations(org_pk):
    organisations = Organisation.objects.filter(parent_organisation_id=org_pk).order_by('name')
    return organisations


@register.assignment_tag
def can_edit_organisation(user, org):
    return org.can_edit(user)


@register.assignment_tag
def get_organisation_leader(org):
    try:
        return org.organisationpost_set.get(user=org.leader)
    except:
        return None


@register.assignment_tag
def get_menu_choices_organisation(user):
    menu_choices = []

    if user.has_perm("organisations.add_organisation"):
        menu_choices.append((_("Lägg till en organisation"), reverse('organisations:create')))

    return menu_choices
