# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0024_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='sponsored',
            field=models.BooleanField(default=False, verbose_name='Sponsrat innehåll?'),
        ),
    ]
