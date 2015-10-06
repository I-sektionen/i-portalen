from django.conf import settings
from django.db import models
from django.utils.http import urlquote
from django.core.validators import RegexValidator


# Create your models here.
class Organisation(models.Model):
    NOT_IN_MENU = "N"
    SEKTIONEN = "S"
    FORENINGAR = "F"
    UTSKOTT = "U"
    ORGANISATION_TYPE_CHOICES = (
        (NOT_IN_MENU, "Inte i menyn"),
        (SEKTIONEN, "Sektionen"),
        (FORENINGAR, "Föreningar"),
        (UTSKOTT, "Utskott"),
    )
    slash_validator = RegexValidator(r'^[^/]+$', "Kan inte innehålla '/'")

    name = models.CharField(max_length=255, unique=True, null=False, validators=[slash_validator])
    description = models.TextField(null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to="organisations", null=True, blank=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="leader")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="members", blank=True)
    organisation_type = models.CharField(max_length=1, choices=ORGANISATION_TYPE_CHOICES, default=NOT_IN_MENU)
    parent_organisation = models.ForeignKey('self', null=True, blank=True, related_name="parent")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/organisations/{:}/".format(urlquote(self.name))