from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django import forms
from django.utils.datastructures import MultiValueDictKeyError
from .models import Article, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('headline', 'lead', 'body', 'visible_from', 'visible_to', 'author', 'tags', 'draft')
        error_messages = {
            'headline': {
                'max_length': _("Titeln är för lång"),
            },
        }
        widgets = {
            'lead': forms.Textarea(attrs={'cols': 65, 'rows': 5}),
            'body': forms.Textarea(attrs={'cols': 65, 'rows': 15, 'class': 'wmd-input', 'id': 'wmd-input-body'}),
            'visible_from': forms.DateTimeInput(),
            'visible_to': forms.DateTimeInput(),
        }

    # This overrides the constructor, and adds the class datetimepicker.
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['visible_from'].widget.attrs['class'] = 'datetimepicker'
        self.fields['visible_to'].widget.attrs['class'] = 'datetimepicker'

    def is_valid(self, **kwargs):
        valid = super(ArticleForm, self).is_valid()

        if not valid:
            return valid

        #Check if the user has permission to add tag.
        u = None
        try:
            if kwargs['user'] is not None:
                u = kwargs['user']
        except KeyError:
            return valid

        has_permission = True
        user_groups = u.groups.all()

        tags = self.cleaned_data["tags"]

        if not tags.exists():
            self.add_error('tags', 'Välj minst en tag.')
            return False

        for tag in tags:
            tag_groups = tag.group.all()
            for tag_group in tag_groups:
                if tag_group not in user_groups:
                    has_permission = False
                    self.add_error('tags', 'Du har inte behörighet att använda {:} tagen.'.format(tag))
                    break
        return has_permission
