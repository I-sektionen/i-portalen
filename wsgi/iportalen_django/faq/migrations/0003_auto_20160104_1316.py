# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_auto_20160103_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.SlugField(max_length=150, unique=True, verbose_name='slug'),
        ),
    ]
