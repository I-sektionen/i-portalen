from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django import forms
from django.utils.datastructures import MultiValueDictKeyError
from .models import Article, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('headline', 'lead', 'body', 'visible_from', 'visible_to', 'tags', 'draft', 'attachment', 'organisations')
        error_messages = {
            'headline': {
                'max_length': _("Titeln är för lång"),
            },
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'wmd-input', 'id': 'wmd-input-body'}),
        }

    # This overrides the constructor, and adds the class datetimepicker.
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['visible_from'].widget.attrs['class'] = 'datetimepicker'
        self.fields['visible_to'].widget.attrs['class'] = 'datetimepicker'
        self.fields['headline'].widget.attrs['placeholder'] = self.fields['headline'].help_text
        self.fields['lead'].widget.attrs['placeholder'] = self.fields['lead'].help_text
        self.fields['body'].widget.attrs['placeholder'] = self.fields['body'].help_text
        self.fields['visible_to'].widget.attrs['placeholder'] = self.fields['visible_to'].help_text
        self.fields['visible_from'].widget.attrs['placeholder'] = self.fields['visible_from'].help_text
        self.fields['draft'].widget.attrs['placeholder'] = self.fields['draft'].help_text
