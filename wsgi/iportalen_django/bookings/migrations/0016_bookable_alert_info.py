# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0015_invoice_issuing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookable',
            name='alert_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
