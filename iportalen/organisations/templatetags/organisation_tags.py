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