# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0009_school_in_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='in_city',
        ),
    ]
