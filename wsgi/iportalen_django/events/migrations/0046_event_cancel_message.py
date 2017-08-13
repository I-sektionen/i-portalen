# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0045_event_cancel'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cancel_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
