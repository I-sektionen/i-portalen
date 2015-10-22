# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20151008_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deregister_delta',
            field=models.PositiveIntegerField(default=1, verbose_name='dagar innan start för senaste avanmälan'),
        ),
    ]
