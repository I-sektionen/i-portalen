from .models import Reward, Period, Evaluation, Course, Year
from django import forms


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['start_date', 'end_date', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['class'] = 'datepicker'
        self.fields['end_date'].widget.attrs['class'] = 'datepicker'


class YearForm(forms.Form):
    year = forms.ChoiceField(label="år", widget=forms.Select, choices=Year.YEAR_CHOICES)
    vt1_start = forms.DateField(label="VT1 start")
    vt2_start = forms.DateField(label="VT2 start")
    vt2_end = forms.DateField(label="VT2 slut")
    ht1_start = forms.DateField(label="HT1 start")
    ht2_start = forms.DateField(label="HT2 start")
    ht2_end = forms.DateField(label="HT2 slut")

    def __init__(self, *args, **kwargs):
        super(YearForm, self).__init__(*args, **kwargs)
        self.fields['vt1_start'].widget.attrs['class'] = 'datepicker'
        self.fields['vt2_start'].widget.attrs['class'] = 'datepicker'
        self.fields['vt2_end'].widget.attrs['class'] = 'datepicker'
        self.fields['ht1_start'].widget.attrs['class'] = 'datepicker'
        self.fields['ht2_start'].widget.attrs['class'] = 'datepicker'
        self.fields['ht2_end'].widget.attrs['class'] = 'datepicker'

    def clean(self):
        super(YearForm, self).clean()
        # year = self.cleaned_data.get("year")  # TODO: make a check that the correct year is choosen
        vt1_start = self.cleaned_data.get("vt1_start")
        vt2_start = self.cleaned_data.get("vt2_start")
        vt2_end = self.cleaned_data.get("vt2_end")
        ht1_start = self.cleaned_data.get("ht1_start")
        ht2_start = self.cleaned_data.get("ht2_start")
        ht2_end = self.cleaned_data.get("ht2_end")
        if vt1_start and vt2_start and vt2_end and ht1_start and ht2_start and ht2_end:
            if vt1_start > vt2_start:
                self.add_error('vt2_start', "VT2 måste börja efter VT1")
            if vt2_start > vt2_end:
                self.add_error('vt2_end', "VT2 måste sluta efter den har börjat")
            if vt2_end > ht1_start:
                self.add_error('ht1_start', "HT1 måste börja efter VT2 slutat")
            if ht1_start > ht2_start:
                self.add_error('ht2_start', "HT2 måste börja efter HT1")
            if ht2_start > ht2_end:
                self.add_error('ht2_end', "HT2 måste sluta efter den har börjat")


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['course', 'reward']

    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
        self.fields['reward'].choices = [(None, "---------")] + [
            (a.pk, str(a)) for a in Reward.objects.filter(active=True)]
        try:
            self.fields['course'].choices = [(None, "---------")] + [
                (a.pk, str(a)) for a in kwargs.get('period').get_free_courses()]
        except:
            pass


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
