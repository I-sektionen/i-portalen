# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0006_auto_20170117_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='id',
            field=models.AutoField(default=datetime.datetime(2017, 1, 17, 13, 48, 34, 305958, tzinfo=utc), primary_key=True, auto_created=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='in_city',
            field=models.ForeignKey(to='exchange_portal.City'),
        ),
    ]
