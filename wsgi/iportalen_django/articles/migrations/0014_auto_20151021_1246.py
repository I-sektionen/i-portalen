# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20151021_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(verbose_name='skribent', max_length=255, help_text='Skribent av texten, fyll bara i detta om ingen organisation valts.'),
        ),
    ]
