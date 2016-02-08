from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Option, Question


class VotingForm(forms.Form):
    options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

    def clean_options(self):
        if len(self.cleaned_data['options']) > Question.objects.get(pk=self.question_id).nr_of_picks:
            raise forms.ValidationError(_('Du har valt för många alternativ.'))
        return self.cleaned_data['options']

    def __init__(self, question_id, *args, **kwargs):
        self.question_id = question_id
        super(VotingForm, self).__init__(*args, **kwargs)
        self.fields['options'].choices = [(a.pk, a.name) for a in Option.objects.filter(question_id=question_id)]
