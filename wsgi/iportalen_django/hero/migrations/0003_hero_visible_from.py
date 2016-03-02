# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.time


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0002_auto_20160302_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='visible_from',
            field=models.DateTimeField(verbose_name='publicering', default=utils.time.now, help_text='Publiceringsdatum'),
        ),
    ]
