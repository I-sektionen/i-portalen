from django.utils.translation import ugettext as _
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('headline', 'lead', 'body', 'visible_from', 'visible_to', 'user', 'tags')
        error_messages = {
            'headline': {
                'max_length': _("Titeln är för lång"),
            },
        }
        widgets = {
            'lead': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'visible_from': forms.DateTimeInput(),
            'visible_to': forms.DateTimeInput(),
        }
