# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0018_auto_20180327_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exchange_course',
            old_name='liu_hp',
            new_name='credits',
        ),
    ]
