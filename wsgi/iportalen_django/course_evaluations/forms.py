from .models import Reward, Period, Evaluation, Course
from django import forms


class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = '__all__'


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = '__all__'


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['course', 'reward']

    def __init__(self, *args, period, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
        self.fields['course'].choices = [(None, "---------")] + [(a.pk, str(a)) for a in period.get_free_courses()]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
