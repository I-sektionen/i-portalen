# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20151111_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DateField(verbose_name='förfallo dag', default=datetime.datetime(2015, 12, 18, 21, 47, 3, 714679)),
        ),
    ]
