# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0056_auto_20180521_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumni_article',
            name='test',
        ),
        migrations.AddField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='Typ', max_length=1, default='a', choices=[('a', 'Artikel'), ('e', 'Event')]),
        ),
    ]
