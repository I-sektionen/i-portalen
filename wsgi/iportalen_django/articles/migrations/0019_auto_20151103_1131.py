# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0018_auto_20151101_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(verbose_name='skribent',
                                   help_text='Skribent av texten visas bara om ingen organisation valts.', null=True,
                                   max_length=255, blank=True),
        ),
    ]
