from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    draft = forms.BooleanField(label="Utkast", required=False)
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['status', 'user', 'created', 'modified', 'replacing']

    # This method add the right class to time/date fields.
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['visible_from'].widget.attrs['class'] = 'datetimepicker'
        self.fields['visible_from'].widget.attrs['placeholder'] = self.fields['visible_from'].help_text



        self.fields['location'].widget.attrs['placeholder'] = self.fields['location'].help_text
        self.fields['start'].widget.attrs['placeholder'] = self.fields['start'].help_text
        self.fields['end'].widget.attrs['placeholder'] = self.fields['end'].help_text

        self.fields['headline'].widget.attrs['placeholder'] = self.fields['headline'].help_text
        self.fields['registration_limit'].widget.attrs['placeholder'] = self.fields['registration_limit'].help_text
        self.fields['deregister_delta'].widget.attrs['placeholder'] = self.fields['deregister_delta'].help_text

        self.fields['lead'].widget.attrs['placeholder'] = self.fields['lead'].help_text



        self.fields['start'].widget.attrs['class'] = 'datetimepicker'
        self.fields['end'].widget.attrs['class'] = 'datetimepicker'
        self.fields['lead'].widget.attrs['cols'] = 40
        self.fields['lead'].widget.attrs['rows'] = 3
        self.fields['body'].widget.attrs['cols'] = 40
        self.fields['body'].widget.attrs['rows'] = 15
        self.fields['body'].widget.attrs['class'] = 'wmd-input'
        self.fields['body'].widget.attrs['id'] = 'wmd-input-body'

    def clean(self):
        super(EventForm, self).clean()
        enable_registration = self.cleaned_data.get("enable_registration")
        registration_limit = self.cleaned_data.get("registration_limit")
        if enable_registration and not registration_limit:
            self.add_error('registration_limit', "Du måste välja ett maximalt antal anmälningar.")




class CheckForm(forms.Form):
    user = forms.CharField()
    force_check_in = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(CheckForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['autofocus'] = "true"


class SpeakerForm(forms.Form):
    speech_nr = forms.CharField(required=False)
    method = forms.CharField()


class ImportEntriesForm(forms.Form):
    users = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "placeholder":"abcde123\nfghij456\nklmno789\n..."}),
        help_text="Ange ett liu-id per rad inga andra tecken är tillåtna."
    )

    def __init__(self, *args, **kwargs):
        super(ImportEntriesForm, self).__init__(*args, **kwargs)
        self.fields['users'].label = "Lista med Liu-id:n att lägga till:"