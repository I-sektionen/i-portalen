# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0021_auto_20151103_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='replacing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True,
                                    to='events.Event', null=True),
        ),
    ]
