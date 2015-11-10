# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0029_auto_20151110_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speakerlist',
            name='next_speaker',
            field=models.ForeignKey(to='events.SpeakerList', default=None, blank=True, null=True),
        ),
    ]
