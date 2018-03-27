# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0017_auto_20180327_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange_course',
            name='level',
            field=models.CharField(max_length=10, default='N/A'),
        ),
        migrations.AddField(
            model_name='exchange_course',
            name='liu_hp',
            field=models.IntegerField(default=0),
        ),
    ]
