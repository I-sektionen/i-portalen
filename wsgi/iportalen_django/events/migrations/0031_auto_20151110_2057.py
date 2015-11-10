# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0030_auto_20151110_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speakerlist',
            name='timestamp',
        ),
        migrations.AlterField(
            model_name='speakerlist',
            name='next_speaker',
            field=models.ForeignKey(to='events.SpeakerList', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, default=None),
        ),
    ]
