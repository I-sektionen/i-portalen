from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['approved', 'user', 'created']

    # This method add the right class to time/date fields.
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['visible_from'].widget.attrs['class'] = 'datetimepicker'
        self.fields['start'].widget.attrs['class'] = 'datetimepicker'
        self.fields['end'].widget.attrs['class'] = 'datetimepicker'
        self.fields['lead'].widget.attrs['cols'] = 40
        self.fields['lead'].widget.attrs['rows'] = 3
        self.fields['body'].widget.attrs['cols'] = 40
        self.fields['body'].widget.attrs['rows'] = 15
        self.fields['body'].widget.attrs['class'] = 'wmd-input'
        self.fields['body'].widget.attrs['id'] = 'wmd-input-body'

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        enable_registration = self.cleaned_data.get("enable_registration")
        registration_limit = self.cleaned_data.get("registration_limit")
        if enable_registration and not registration_limit:
            self.add_error('registration_limit', "Du måste välja ett maximalt antal anmälningar.")


class CheckForm(forms.Form):
    liu = forms.CharField(max_length=10)
    force_check_in = forms.BooleanField(required=False)
