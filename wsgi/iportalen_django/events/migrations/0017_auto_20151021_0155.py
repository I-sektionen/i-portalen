# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0016_event_organisations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organisations',
            field=models.ManyToManyField(default=None, help_text='Organisation/organisationer som artikeln hör till',
                                         blank=True, to='organisations.Organisation', verbose_name='organisationer'),
        ),
    ]
