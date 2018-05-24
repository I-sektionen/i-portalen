# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0027_auto_20180503_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iuser',
            name='date_gdpr_accepted',
            field=models.DateTimeField(null=True, blank=True, verbose_name='accepterade villkoren datum'),
        ),
    ]
