__author__ = 'isac'
from django import forms
from .models import Booking, BookingSlot


"""
- Bookable is already selected in prior step.
- The selected User is the logged in user TODO: add groups.
- Form should present a timespan
"""


class NewBookingForm(forms.Form):
    forms.CharField(max_length=300)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['bookable', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class BookingSlotForm(forms.ModelForm):
    class Meta:
        model = BookingSlot
        fields = ['bookable', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
