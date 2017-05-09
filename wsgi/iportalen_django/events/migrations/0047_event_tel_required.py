# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0046_event_cancel_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tel_required',
            field=models.BooleanField(default=False, help_text='Kryssa i om telefonnummer krävs', verbose_name='telefonnummer krävs'),
        ),
    ]
