# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0004_auto_20151118_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookable',
            name='max_number_of_slots_in_booking',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='bookable',
            name='max_number_of_bookings',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DateField(verbose_name='förfallo dag',
                                   default=datetime.datetime(2015, 12, 21, 1, 31, 3, 958756)),
        ),
    ]
