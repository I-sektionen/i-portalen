# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0006_auto_20151018_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='iuser',
            name='is_member',
            field=models.NullBooleanField(default=None, verbose_name='Är medlem?'),
        ),
    ]
