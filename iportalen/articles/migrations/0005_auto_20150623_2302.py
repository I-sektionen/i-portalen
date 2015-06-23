# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20150623_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='visible_from',
            field=models.DateTimeField(verbose_name='publicera från', default=datetime.datetime(2015, 6, 23, 23, 2, 57, 450146)),
        ),
    ]
