# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0032_event_sponsored'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='sponsored',
            field=models.BooleanField(default=False, help_text='Kryssa i om innehållet är sponsrat', verbose_name='sponsrat'),
        ),
    ]
