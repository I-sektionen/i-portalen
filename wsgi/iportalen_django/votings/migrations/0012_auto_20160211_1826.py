# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0011_auto_20160211_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='min_nr_of_picks',
            field=models.IntegerField(default=0, verbose_name='Min antal val en användare kan kryssa i på frågan.'),
        ),
        migrations.AlterField(
            model_name='question',
            name='nr_of_picks',
            field=models.IntegerField(default=1, verbose_name='Max antal val en användare kan kryssa i på frågan.'),
        ),
    ]
