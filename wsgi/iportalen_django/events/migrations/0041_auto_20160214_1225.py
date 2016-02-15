# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0040_auto_20160213_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deregister_delta',
            field=models.PositiveIntegerField(verbose_name='Sista dag för anmälan/avanmälan', default=1, help_text='Sista dag för anmälan/avanmälan i antal dagar innan eventet'),
        ),
    ]
