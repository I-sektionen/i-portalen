from django import forms
from django.utils import timezone
from .models import Event


class EventForm(forms.ModelForm):
    draft = forms.BooleanField(label="Utkast", required=False, help_text="Sparar utan att publicera")

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
        self.fields['extra_deadline'].widget.attrs['placeholder'] = self.fields['extra_deadline'].help_text
        self.fields['extra_deadline_text'].widget.attrs['placeholder'] = self.fields['extra_deadline_text'].help_text

        self.fields['headline'].widget.attrs['placeholder'] = self.fields['headline'].help_text
        self.fields['registration_limit'].widget.attrs['placeholder'] = self.fields['registration_limit'].help_text
        self.fields['deregister_delta'].widget.attrs['placeholder'] = self.fields['deregister_delta'].help_text

        self.fields['lead'].widget.attrs['placeholder'] = self.fields['lead'].help_text

        self.fields['start'].widget.attrs['class'] = 'datetimepicker'
        self.fields['end'].widget.attrs['class'] = 'datetimepicker'
        self.fields['extra_deadline'].widget.attrs['class'] = 'datetimepicker'
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
        if registration_limit and not enable_registration:
            self.add_error('enable_registration',
                           "Du ha valt ett maximalt antal anmälningar "
                           "men inte kryssat i rutan för att tillåta anmälningar")
        end = self.cleaned_data.get("end")
        start = self.cleaned_data.get("start")
        visible_from = self.cleaned_data.get("visible_from")
        if end:
            if visible_from:
                if end < visible_from:
                    self.add_error('end', "Datumet måste vara före publiceringsdatumet.")
            if start:
                if start > end:
                    self.add_error('start', "Datumet måste vara före slut datumet.")
            if end < timezone.now():
                self.add_error('end', "Datumet måste vara före dagens datum.")


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
        widget=forms.Textarea(attrs={"rows": 15, "placeholder": "abcde123\nfghij456\nklmno789\n..."}),
        help_text="Ange ett liu-id per rad inga andra tecken är tillåtna."
    )

    def __init__(self, *args, **kwargs):
        super(ImportEntriesForm, self).__init__(*args, **kwargs)
        self.fields['users'].label = "Lista med Liu-id:n att lägga till:"
