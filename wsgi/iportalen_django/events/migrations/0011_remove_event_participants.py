# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20151007_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
    ]
