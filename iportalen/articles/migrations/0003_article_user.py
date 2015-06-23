# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0002_remove_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
    ]
