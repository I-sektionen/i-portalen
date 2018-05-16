# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0021_auto_20180503_1739'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Stad', 'verbose_name_plural': 'Städer', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='continent',
            options={'verbose_name': 'Världsdel', 'verbose_name_plural': 'Världsdelar', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Land', 'verbose_name_plural': 'Länder', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='exchange_course',
            options={'verbose_name': 'Utlandskurs', 'verbose_name_plural': 'Utlandskurser', 'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='school',
            options={'verbose_name': 'Skola', 'verbose_name_plural': 'Skolor', 'ordering': ['name']},
        ),
    ]
