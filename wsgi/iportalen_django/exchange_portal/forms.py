from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }
