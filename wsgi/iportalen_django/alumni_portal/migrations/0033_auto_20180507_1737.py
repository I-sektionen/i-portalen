# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0032_auto_20180507_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='Typ', max_length=12, default='E', choices=[('A', 'Artikel'), ('E', 'Event')]),
        ),
    ]
