from django import forms
from .models import Hero


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ('file', 'visible_from')