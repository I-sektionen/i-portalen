# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('articles', '0007_article_replacing'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='group',
            field=models.ManyToManyField(blank=True, to='auth.Group', null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='replacing',
            field=models.ForeignKey(blank=True, to='articles.Article', default=None, null=True),
        ),
    ]
