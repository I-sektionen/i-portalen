# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-01 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0015_auto_20160101_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'man'), ('w', 'kvinna'), ('o', 'Annat / Icke-binär'), ('u', 'Vill ej ange')], default=None, max_length=1, null=True, verbose_name='kön'),
        ),
    ]
