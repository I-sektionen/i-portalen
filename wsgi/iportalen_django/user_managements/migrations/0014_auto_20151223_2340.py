# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 22:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0013_auto_20151223_1810'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ipikuresubscriber',
            options={'permissions': (('can_view_subscribers', 'Can view subscribers'),), 'verbose_name': 'ipikureprenumerant', 'verbose_name_plural': 'ipikureprenumeranter'},
        ),
    ]
