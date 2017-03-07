# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0003_auto_20170307_1731'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='exhange_with_liu',
            new_name='exchange_with_liu',
        ),
    ]
