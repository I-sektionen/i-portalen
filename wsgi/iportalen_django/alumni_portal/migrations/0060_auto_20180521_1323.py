# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0059_alumni_article'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumni_article',
            options={'verbose_name': 'Artikel/Event', 'verbose_name_plural': 'Artiklar/Event', 'permissions': (('can_approve_article', 'Can approve article'),)},
        ),
    ]
