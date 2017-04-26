
from django.db import models

# Create your models here.
from fika_penalty.managers import FikaPenaltyManager
from organisations.models import Organisation
from user_managements.models import IUser


class FikaPenalty(models.Model):
    user = models.ForeignKey(IUser, verbose_name="Medlem")
    organisation = models.ForeignKey(Organisation)
    cost = models.FloatField(verbose_name="Kostnad", help_text="För att bokföra en inbetalning sätt ett minustecken först. ex -100")
    date = models.DateField(verbose_name="Datum")
    reason = models.TextField(verbose_name="Anledning", null=True, blank=True)

    objects = FikaPenaltyManager()

    def __str__(self):
        return "{name} - {org}".format(name=self.user.get_full_name, org=str(self.organisation))

