# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0031_auto_20160205_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='attachment',
        ),
    ]
