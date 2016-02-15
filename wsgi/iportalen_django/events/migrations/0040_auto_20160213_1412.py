# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0039_remove_event_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speakerlist',
            name='event',
        ),
        migrations.RemoveField(
            model_name='speakerlist',
            name='next_speaker',
        ),
        migrations.RemoveField(
            model_name='speakerlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='SpeakerList',
        ),
    ]
