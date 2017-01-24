# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0008_remove_school_in_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='in_city',
            field=models.ForeignKey(default=datetime.datetime(2017, 1, 17, 14, 10, 49, 632802, tzinfo=utc), to='exchange_portal.City'),
            preserve_default=False,
        ),
    ]
