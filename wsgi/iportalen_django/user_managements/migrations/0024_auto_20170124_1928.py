# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0023_auto_20170124_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iuser',
            name='modified',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2016, 1, 25, 18, 28, 10, 498943, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
