# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-13 23:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_evaluations', '0004_auto_20151213_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='active',
            field=models.BooleanField(default=True, verbose_name='aktiv'),
        ),
        migrations.AlterField(
            model_name='period',
            name='name',
            field=models.CharField(choices=[('VT1', 'VT1'), ('VT2', 'VT2'), ('HT1', 'HT1'), ('HT2', 'HT2')], help_text='Ex, VT1', max_length=255, verbose_name='namn'),
        ),
    ]
