# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20150731_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custominvoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 8, 30, 15, 16, 52, 153771)),
        ),
        migrations.AlterField(
            model_name='userinvoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 8, 30, 15, 16, 52, 153771)),
        ),
    ]
