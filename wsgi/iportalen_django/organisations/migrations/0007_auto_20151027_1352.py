# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0006_auto_20151020_2223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organisation',
            options={'verbose_name': 'organisation', 'verbose_name_plural': 'organisationer'},
        ),
    ]
