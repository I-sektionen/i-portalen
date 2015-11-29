# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0014_auto_20151021_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(blank=True, null=True, max_length=255,
                                   help_text='Skribent av texten, fyll bara i detta om ingen organisation valts.',
                                   verbose_name='skribent'),
        ),
    ]
