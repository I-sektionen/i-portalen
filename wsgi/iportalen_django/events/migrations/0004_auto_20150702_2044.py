# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150702_2036'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entrydeadline',
            old_name='description_sv',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_limit',
            field=models.IntegerField(null=True, verbose_name='max antal anmälningar', blank=True),
        ),
    ]
