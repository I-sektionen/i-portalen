from django.db import models
from django.db.models import Sum


class FikaPenaltyManager(models.Manager):
    def get_sum_per_organisation(self, organisation):
        return self.filter(organisation=organisation, paid=False).aggregate(Sum('cost'))