# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0037_auto_20180507_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='Typ', max_length=20, blank=True, default=('A', 'Artikel'), choices=[('A', 'Artikel'), ('E', 'Event')]),
        ),
    ]
