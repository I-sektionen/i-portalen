# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_auto_20151108_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='speakerlist',
            name='first',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='speakerlist',
            name='next_speaker',
            field=models.ForeignKey(to='events.SpeakerList', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='extra_deadline_text',
            field=models.CharField(verbose_name='beskrivning till det extra anmälningsstoppet', max_length=255, help_text='Ex. få mat, garanteras fika osv. Lämna tomt om extra anmälningsstopp ej angivits.', blank=True, null=True),
        ),
    ]
