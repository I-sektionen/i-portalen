# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.time


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0007_auto_20151126_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DateField(default=utils.time.now_plus_one_month, verbose_name='förfallo dag'),
        ),
    ]
