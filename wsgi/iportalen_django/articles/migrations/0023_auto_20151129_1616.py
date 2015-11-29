# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.time


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_auto_20151129_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='visible_from',
            field=models.DateTimeField(default=utils.time.now, verbose_name='publicering', help_text='Publiceringsdatum'),
        ),
    ]
