# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0053_auto_20180521_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni_article',
            name='test',
            field=models.CharField(verbose_name='test', max_length=1, default='b'),
        ),
    ]
