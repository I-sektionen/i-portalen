# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0005_auto_20151121_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DateField(verbose_name='förfallo dag',
                                   default=datetime.datetime(2015, 12, 23, 18, 27, 32, 830462)),
        ),
    ]
