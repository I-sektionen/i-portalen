# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speaker_list', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speakerlist',
            name='first',
        ),
        migrations.RemoveField(
            model_name='speakerlist',
            name='next_speaker',
        ),
        migrations.AddField(
            model_name='speakerlist',
            name='has_spoken',
            field=models.BooleanField(default=False, verbose_name='har talat?'),
        ),
        migrations.AddField(
            model_name='speakerlist',
            name='nr_of_speeches',
            field=models.IntegerField(default=1, verbose_name='antal talade gånger'),
        ),
        migrations.AddField(
            model_name='speakerlist',
            name='speech_id',
            field=models.IntegerField(default=1, verbose_name='talar id'),
        ),
    ]
