from django.utils import timezone
from django.db import models, transaction


class YearManager(models.Manager):
    @transaction.atomic
    def copy_last_year(self):
        last_year = self.all().order_by('-year')[0]
        new_year = self.model(year=last_year.year+1)
        new_year.add_periods(vt1_start=last_year.ht2.end_date,
                             vt2_start=last_year.vt2.start_date+timezone.timedelta(days=365),
                             vt2_end=last_year.vt2.end_date+timezone.timedelta(days=365),
                             ht1_start=last_year.ht1.end_date+timezone.timedelta(days=365),
                             ht2_start=last_year.ht2.start_date+timezone.timedelta(days=365),
                             ht2_end=last_year.ht2.end_date+timezone.timedelta(days=365))
        for c in last_year.vt1.courses.all():
            new_year.vt1.courses.add(c)
        for c in last_year.vt2.courses.all():
            new_year.vt2.courses.add(c)
        for c in last_year.ht1.courses.all():
            new_year.ht1.courses.add(c)
        for c in last_year.ht2.courses.all():
            new_year.ht2.courses.add(c)
        return new_year
