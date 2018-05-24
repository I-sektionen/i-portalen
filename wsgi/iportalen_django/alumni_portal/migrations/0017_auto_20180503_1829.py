# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0016_auto_20180503_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='typ', max_length=1, default='Article', choices=[('Article', 'Artiklar'), ('Event', 'Event')], help_text='Article för artikel eller Event för event'),
        ),
    ]
