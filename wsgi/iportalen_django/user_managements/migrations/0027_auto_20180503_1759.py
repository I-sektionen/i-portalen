# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0026_auto_20180503_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iuser',
            name='date_gdpr_accepted',
            field=models.DateTimeField(verbose_name='accepterade villkoren datum', null=True),
        ),
    ]
