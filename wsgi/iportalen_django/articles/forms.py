from django.utils.translation import ugettext as _
from django.forms import ModelForm, Textarea, DateTimeInput
from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('headline', 'lead', 'body', 'visible_from', 'visible_to', 'user', 'tags')
        error_messages = {
            'headline': {
                'max_length': _("Titeln är för lång"),
            },
        }
        widgets = {
            'lead': Textarea(attrs={'cols': 80, 'rows': 20}),
            'body': Textarea(attrs={'cols': 80, 'rows': 20}),
            'visible_from': DateTimeInput(),
            'visible_to': DateTimeInput(format=['%Y-%m-%d %H:%M:%S']),
        }
