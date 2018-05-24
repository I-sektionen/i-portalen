# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0055_remove_alumni_article_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='test',
            field=models.CharField(verbose_name='test', max_length=2, default='b'),
        ),
    ]
