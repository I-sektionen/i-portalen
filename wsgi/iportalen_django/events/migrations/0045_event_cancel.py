# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0044_auto_20160306_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cancel',
            field=models.CharField(blank=True, verbose_name='Beskrivning för inställt event', null=True, help_text='Motivera varför eventet blivit inställt', max_length=255),
        ),
    ]
