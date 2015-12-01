# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_auto_20151103_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='visible_from',
            field=models.DateTimeField(help_text='Publiceringsdatum', verbose_name='publicering', default=django.utils.timezone.now),
        ),
    ]
