# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speaker_list', '0003_auto_20160213_1850'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='speakerlist',
            options={'ordering': ['nr_of_speeches', 'speech_id']},
        ),
        migrations.AlterField(
            model_name='speakerlist',
            name='speech_id',
            field=models.IntegerField(verbose_name='talar id', default=1),
        ),
    ]
