# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0003_hero_visible_from'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hero',
            options={'ordering': ['visible_from'], 'verbose_name_plural': 'Herosarna', 'verbose_name': 'Hero'},
        ),
    ]
