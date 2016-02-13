# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speaker_list', '0002_auto_20160213_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speakerlist',
            name='speech_id',
            field=models.IntegerField(default=1, unique=True, verbose_name='talar id'),
        ),
    ]
