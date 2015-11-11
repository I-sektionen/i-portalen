# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20151012_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='group',
        ),
    ]
