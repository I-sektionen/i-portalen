# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0030_auto_20160203_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(max_length=1, choices=[('d', 'Utkast'), ('b', 'väntar på godkännande'), ('r', 'Avslaget'), ('a', 'Godkännt')], default='d'),
        ),
    ]
