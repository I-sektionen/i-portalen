# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0010_auto_20151223_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='ocr',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='OCR nummer'),
        ),
    ]
