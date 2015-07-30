# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookable',
            name='max_number_of_bookings',
            field=models.IntegerField(default=3, max_length=100),
            preserve_default=False,
        ),
    ]
