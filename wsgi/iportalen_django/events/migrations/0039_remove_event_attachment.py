# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_auto_20160207_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='attachment',
        ),
    ]
