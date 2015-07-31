# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_auto_20150731_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custominvoice',
            name='booking',
            field=models.ForeignKey(to='bookings.Booking'),
        ),
        migrations.AlterField(
            model_name='custominvoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 8, 30, 15, 20, 37, 84441)),
        ),
        migrations.AlterField(
            model_name='userinvoice',
            name='booking',
            field=models.ForeignKey(to='bookings.Booking'),
        ),
        migrations.AlterField(
            model_name='userinvoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 8, 30, 15, 20, 37, 84441)),
        ),
    ]
