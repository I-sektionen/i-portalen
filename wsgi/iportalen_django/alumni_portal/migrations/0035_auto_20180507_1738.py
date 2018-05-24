# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0034_auto_20180507_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='Typ', max_length=12, blank=True, default=None, choices=[('A', 'Artikel'), ('E', 'Event')]),
        ),
    ]
