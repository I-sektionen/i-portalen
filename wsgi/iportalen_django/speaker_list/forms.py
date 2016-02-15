from django import forms


class SpeakerForm(forms.Form):
    speech_nr = forms.CharField(required=False)
    method = forms.CharField()

