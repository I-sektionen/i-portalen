# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0024_auto_20170124_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iuser',
            name='p_nr',
        ),
    ]
