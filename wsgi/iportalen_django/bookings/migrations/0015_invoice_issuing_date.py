# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0014_bookable_require_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='issuing_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='fakturerings datum'),
        ),
    ]
