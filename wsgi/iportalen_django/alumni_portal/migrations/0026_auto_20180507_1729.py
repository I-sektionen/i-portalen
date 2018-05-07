# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0025_auto_20180503_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='Typ', max_length=1, default=None, choices=[('A', 'Artikel'), ('E', 'Event')], help_text='Välj ifall det är en artikel eller ett event'),
        ),
    ]
