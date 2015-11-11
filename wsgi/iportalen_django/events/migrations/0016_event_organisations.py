# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0006_auto_20151020_2223'),
        ('events', '0015_auto_20151020_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organisations',
            field=models.ManyToManyField(verbose_name='organisationer', help_text='Organisation/organisationer som artikeln hör till', null=True, blank=True, to='organisations.Organisation', default=None),
        ),
    ]
