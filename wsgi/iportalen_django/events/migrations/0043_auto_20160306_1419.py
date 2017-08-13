# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0042_auto_20160215_2024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Arrangemang', 'verbose_name_plural': 'Arrangemang', 'permissions': (('can_approve_event', 'Can approve event'), ('can_view_no_shows', 'Can view no shows'), ('can_remove_no_shows', 'Can remove no shows'))},
        ),
    ]
