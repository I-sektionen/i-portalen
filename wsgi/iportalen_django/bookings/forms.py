__author__ = 'isac'
from django import forms
from .models import Booking


class MakeBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'slot']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
