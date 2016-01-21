# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0013_auto_20160116_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookable',
            name='require_phone',
            field=models.BooleanField(default=False),
        ),
    ]
