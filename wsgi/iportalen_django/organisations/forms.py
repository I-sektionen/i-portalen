from django import forms

from .models import Organisation


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ('description', 'contact_info', 'leader', 'image')


    # This method add the right class to time/date fields.
    #def __init__(self, *args, **kwargs):
