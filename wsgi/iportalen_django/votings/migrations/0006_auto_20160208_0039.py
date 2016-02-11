# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0005_auto_20160207_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='result',
        ),
        migrations.AddField(
            model_name='question',
            name='publish_results',
            field=models.CharField(default='c', max_length=1, choices=[('b', 'Gör resultaten synliga innan man röstat.'), ('a', 'Gör resultaten synliga efter att man röstat.'), ('c', 'Gör resultaten synliga när röstningen stängt.')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='anonymous',
            field=models.BooleanField(default=True, verbose_name='anonym'),
        ),
    ]
