# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_article_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='replacing',
            field=models.ForeignKey(null=True, to='articles.Article', default=None),
        ),
    ]
