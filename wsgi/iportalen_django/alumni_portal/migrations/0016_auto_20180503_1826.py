# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0015_auto_20180503_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.TextField(verbose_name='typ', max_length=10, default='a', choices=[('Article', 'Artiklar'), ('Event', 'Event')], help_text='Article för artikel eller Event för event'),
        ),
    ]
