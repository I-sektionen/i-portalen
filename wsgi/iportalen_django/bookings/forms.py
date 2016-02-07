from django import forms


class BookingForm(forms.Form):
    start = forms.ChoiceField()
    end = forms.ChoiceField()
