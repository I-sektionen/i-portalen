# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0002_auto_20150702_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='iuser',
            name='rfid_number',
            field=models.CharField(null=True, verbose_name='rfid', max_length=255, blank=True),
        ),
    ]
