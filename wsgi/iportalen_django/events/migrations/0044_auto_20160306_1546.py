# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0043_auto_20160306_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(default='d', max_length=1, choices=[('d', 'utkast'), ('b', 'väntar på godkännande'), ('r', 'Avslaget'), ('a', 'Godkänt'), ('c', 'Inställt'), ('e', 'väntar på att bli inställd')]),
        ),
    ]
