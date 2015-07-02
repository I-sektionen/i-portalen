# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150702_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='registration_limit',
            field=models.IntegerField(null=True, verbose_name='max antal anmälningar'),
        ),
    ]
