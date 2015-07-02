# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bachelorprofile',
            name='info',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bachelorprofile',
            name='link',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='masterprofile',
            name='info',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='masterprofile',
            name='link',
            field=models.URLField(null=True, blank=True),
        ),
    ]
