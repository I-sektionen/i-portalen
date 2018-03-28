# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0002_auto_20170124_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='exhange_with_liu',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='school',
            name='freemover',
            field=models.BooleanField(default=False),
        ),
    ]
