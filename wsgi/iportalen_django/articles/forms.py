from django.utils import timezone
from django.utils.translation import ugettext as _
from django import forms
from .models import Article, OtherAttachment, ImageAttachment


class ArticleForm(forms.ModelForm):
    draft = forms.BooleanField(label="Utkast", required=False, help_text="Sparar utan att publicera")

    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['status', 'user', 'created', 'modified', 'replacing']
        error_messages = {
            'headline': {
                'max_length': _("Titeln är för lång"),
            },
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'wmd-input', 'id': 'wmd-input-body'}),
        }

    def __init__(self, *args, **kwargs):
        """This overrides the constructor, and adds the class datetimepicker."""
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['visible_from'].widget.attrs['class'] = 'datetimepicker'
        self.fields['visible_to'].widget.attrs['class'] = 'datetimepicker'
        self.fields['headline'].widget.attrs['placeholder'] = self.fields['headline'].help_text
        self.fields['lead'].widget.attrs['placeholder'] = self.fields['lead'].help_text
        self.fields['body'].widget.attrs['placeholder'] = self.fields['body'].help_text
        self.fields['visible_to'].widget.attrs['placeholder'] = self.fields['visible_to'].help_text
        self.fields['visible_from'].widget.attrs['placeholder'] = self.fields['visible_from'].help_text

    def clean(self):
        super(ArticleForm, self).clean()
        visible_to = self.cleaned_data.get("visible_to")
        visible_from = self.cleaned_data.get("visible_from")
        if visible_to:
            if visible_from:
                if visible_to < timezone.now():
                    self.add_error('visible_to', "Datumet måste vara före dagens datum.")
            if visible_to < visible_from:
                self.add_error('visible_to', "Datumet måste vara före publiceringsdatumet.")


class RejectionForm(forms.Form):
    rejection_message = forms.CharField(label="Avslagsmeddelande", widget=forms.Textarea())


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = OtherAttachment
        fields = ('file', 'display_name')


class ImageAttachmentForm(forms.ModelForm):
    class Meta:
        model = ImageAttachment
        fields = ('img', 'caption')
