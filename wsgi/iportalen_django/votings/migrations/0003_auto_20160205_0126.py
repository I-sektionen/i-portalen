# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0002_auto_20160205_0112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_status',
            new_name='status',
        ),
    ]
