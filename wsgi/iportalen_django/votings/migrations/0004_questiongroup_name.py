# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0003_auto_20160205_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiongroup',
            name='name',
            field=models.CharField(verbose_name='namn', max_length=255, null=True, blank=True),
        ),
    ]
