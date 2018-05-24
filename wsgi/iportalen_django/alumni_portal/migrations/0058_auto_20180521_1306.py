# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0057_auto_20180521_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumni_article',
            name='organisations',
        ),
        migrations.RemoveField(
            model_name='alumni_article',
            name='replacing',
        ),
        migrations.RemoveField(
            model_name='alumni_article',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='alumni_article',
            name='user',
        ),
        migrations.DeleteModel(
            name='Alumni_Article',
        ),
    ]
