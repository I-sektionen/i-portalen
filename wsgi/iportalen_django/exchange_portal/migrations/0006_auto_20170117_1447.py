# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0005_auto_20170117_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='id',
        ),
        migrations.AlterField(
            model_name='school',
            name='in_city',
            field=models.ForeignKey(to='exchange_portal.City', serialize=False, primary_key=True),
        ),
    ]
