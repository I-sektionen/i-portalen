# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_auto_20151110_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speakerlist',
            name='first',
            field=models.NullBooleanField(default=None),
        ),
    ]
