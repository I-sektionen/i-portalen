# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hero',
            options={'verbose_name': 'Hero', 'verbose_name_plural': 'Herosarna', 'ordering': ['modified']},
        ),
        migrations.AddField(
            model_name='hero',
            name='modified',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2016, 3, 2, 17, 31, 53, 12478, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
