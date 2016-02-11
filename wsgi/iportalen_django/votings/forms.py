from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from .models import Option, Question


class VotingForm(forms.Form):
    options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False)
    verification = forms.CharField(label=_("Verifikationskod"), max_length=255, required=False)

    def clean_options(self):
        if len(self.cleaned_data['options']) > Question.objects.get(pk=self.question_id).nr_of_picks:
            raise forms.ValidationError(_('Du har valt för många alternativ.'))
        elif len(self.cleaned_data['options']) < Question.objects.get(pk=self.question_id).min_nr_of_picks:
            raise forms.ValidationError(_('Du har valt för få alternativ.'))
        return self.cleaned_data['options']

    def clean_verification(self):
        if self.cleaned_data['verification'] != Question.objects.get(pk=self.question_id).verification:
            raise forms.ValidationError(_('Fel verifikationskod.'))
        return self.cleaned_data['verification']

    def __init__(self, question_id, *args, **kwargs):
        self.question_id = question_id
        q = get_object_or_404(Question, pk=question_id)
        super(VotingForm, self).__init__(*args, **kwargs)

        if q.verification:
            self.fields['verification'].required = True
        self.fields['options'].choices = [(a.pk, a.name) for a in Option.objects.filter(question_id=question_id)]
