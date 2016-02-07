# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0037_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'Arrangemang', 'verbose_name': 'Arrangemang', 'permissions': (('can_approve_event', 'Can approve event'), ('can_view_no_shows', 'Can view no shows'))},
        ),
    ]
