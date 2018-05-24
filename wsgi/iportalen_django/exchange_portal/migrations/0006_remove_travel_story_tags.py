# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0005_auto_20171121_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_story',
            name='tags',
        ),
    ]
