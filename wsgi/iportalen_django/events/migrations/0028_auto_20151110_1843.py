# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_auto_20151110_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speakerlist',
            name='first',
            field=models.BooleanField(),
        ),
    ]
