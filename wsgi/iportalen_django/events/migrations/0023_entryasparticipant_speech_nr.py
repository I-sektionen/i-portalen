# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_event_replacing'),
    ]

    operations = [
        migrations.AddField(
            model_name='entryasparticipant',
            name='speech_nr',
            field=models.PositiveIntegerField(verbose_name='talar nummer', null=True, blank=True),
        ),
    ]
