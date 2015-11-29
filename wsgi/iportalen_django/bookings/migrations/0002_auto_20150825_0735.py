# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('CR', 'Skapad'), ('SE', 'Skickad'), ('TR', 'Avbruten'), ('PA', 'Betald')],
                                   default='CR', max_length=2),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 9, 24, 7, 35, 14, 691931)),
        ),
    ]
