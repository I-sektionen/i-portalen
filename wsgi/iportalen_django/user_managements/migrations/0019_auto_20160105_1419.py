# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 13:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0018_auto_20160104_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipikuresubscriber',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]