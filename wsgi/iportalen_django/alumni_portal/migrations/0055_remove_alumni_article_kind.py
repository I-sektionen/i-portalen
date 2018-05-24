# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0054_alumni_article_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumni_article',
            name='kind',
        ),
    ]
