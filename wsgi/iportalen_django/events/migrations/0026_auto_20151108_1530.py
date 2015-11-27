# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0025_event_extra_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='extra_deadline_text',
            field=models.CharField(null=True, help_text='Lämna tomt om extra anmälningsstopp ej angivits.',
                                   verbose_name='Beskrivning till det extra anmälningsstoppet', blank=True,
                                   max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='extra_deadline',
            field=models.DateTimeField(null=True,
                                       help_text='Exempelvis: Datum att anmäla sig innan för att få mat. '
                                                 'Kan lämnas tomt.',
                                       verbose_name='extra anmälningsstopp', blank=True),
        ),
    ]
