# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0007_auto_20170117_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='in_city',
        ),
    ]
