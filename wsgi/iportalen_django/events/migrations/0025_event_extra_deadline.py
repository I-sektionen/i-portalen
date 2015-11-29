# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0024_speakerlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='extra_deadline',
            field=models.DateTimeField(null=True, blank=True, verbose_name='extra anmälningsstopp',
                                       help_text='Exempelvis: Datum att anmäla sig innan för att få mat.'),
        ),
    ]
