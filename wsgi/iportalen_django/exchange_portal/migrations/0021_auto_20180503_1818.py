# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0020_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='message',
            new_name='feedback',
        ),
    ]
