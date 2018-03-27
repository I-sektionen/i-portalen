# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0016_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='liu_course',
            name='level',
            field=models.CharField(max_length=10, default='N/A'),
        ),
        migrations.AddField(
            model_name='liu_course',
            name='liu_hp',
            field=models.IntegerField(default=0),
        ),
    ]
