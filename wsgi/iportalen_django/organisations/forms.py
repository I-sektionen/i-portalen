from django import forms
from .models import Organisation, OrganisationPost


class OrganisationForm(forms.ModelForm):

    class Meta:
        model = Organisation
        fields = ('description', 'contact_info', 'leader', 'image')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'wmd-input', 'id': 'wmd-input-body'}),
        }
        # This method add the right class to time/date fields.
        # def __init__(self, *args, **kwargs):


class AddOrganisationForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Organisation
        fields = ('name', 'leader', 'organisation_type', 'parent_organisation', 'group')
