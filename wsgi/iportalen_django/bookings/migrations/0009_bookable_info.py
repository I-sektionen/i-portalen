# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 22:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_auto_20151129_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookable',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
