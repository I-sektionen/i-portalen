# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0033_auto_20160215_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageattachment',
            name='caption',
            field=models.CharField(max_length=100, verbose_name='Bildrubrik'),
        ),
    ]
