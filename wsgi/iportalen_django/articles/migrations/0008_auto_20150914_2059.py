# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_remove_event_tags'),
        ('articles', '0007_article_replacing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.AlterField(
            model_name='article',
            name='replacing',
            field=models.ForeignKey(to='articles.Article', blank=True, null=True, default=None),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
