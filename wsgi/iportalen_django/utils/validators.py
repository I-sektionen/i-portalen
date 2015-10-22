__author__ = 'jonathan'
from django.core.validators import RegexValidator

liu_id_validator = RegexValidator(r'^[a-zA-Z]{5}\d{3}$')
slash_validator = RegexValidator(r'^[^/]+$', "Kan inte innehålla '/'")