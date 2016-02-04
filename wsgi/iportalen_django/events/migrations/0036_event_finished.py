# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0035_event_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='Avsluta event', help_text='Kryssa i om eventet ska avslutas'),
        ),
    ]
