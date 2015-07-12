# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='name_sv',
            new_name='name',
        ),
    ]
