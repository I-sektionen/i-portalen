# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0019_auto_20180327_1940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='travel_story',
            options={'verbose_name': 'Reseberättelse', 'verbose_name_plural': 'Reseberättelser', 'ordering': ['year_abroad', 'term_abroad']},
        ),
    ]
