
from django.db import models

# Create your models here.
from organisations.models import Organisation
from user_managements.models import IUser


class FikaPenalty(models.Model):
    user = models.ForeignKey(IUser)
    organisation = models.ForeignKey(Organisation)
    cost = models.FloatField(verbose_name="Kostnad")
    date = models.DateField(verbose_name="Datum")
    reason = models.TextField(verbose_name="Anledning", null=True, blank=True)
    paid = models.BooleanField(default=False, verbose_name="Betald")

    def __str__(self):
        return "{name} - {org}".format(name=self.user.get_full_name, org=str(self.organisation))

    def pay(self):
        self.paid = True
        self.save()
