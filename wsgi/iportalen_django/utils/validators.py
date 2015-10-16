__author__ = 'jonathan'
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .text import count_words, count_characters

liu_id_validator = RegexValidator(r'^[a-zA-Z]{5}\d{3}$')
slash_validator = RegexValidator(r'^[^/]+$', "Kan inte innehålla '/'")

def less_than_200_words_validator(value):
    if count_words(value) > 201:
        raise ValidationError('För många ord.')

def less_than_160_characters_validator(value):
    if count_characters(value) > 160:
        raise ValidationError('För många tecken.')