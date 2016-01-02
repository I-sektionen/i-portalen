# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0006_auto_20151123_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookable',
            name='hours_before_booking',
            field=models.IntegerField(default=24),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DateField(verbose_name='förfallo dag',
                                   default=datetime.datetime(2015, 12, 26, 16, 8, 31, 91765)),
        ),
    ]
