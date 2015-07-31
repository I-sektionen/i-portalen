# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_auto_20150731_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custominvoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 8, 30, 18, 55, 3, 917375)),
        ),
        migrations.AlterField(
            model_name='fixedcosttemplate',
            name='tax',
            field=models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userinvoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 8, 30, 18, 55, 3, 917375)),
        ),
        migrations.AlterField(
            model_name='variablecosttemplate',
            name='tax',
            field=models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True),
        ),
    ]
