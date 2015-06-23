# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0003_auto_20150623_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bachelorprofile',
            name='name',
            field=models.CharField(verbose_name='namn', max_length=255),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='date_joined',
            field=models.DateTimeField(verbose_name='gick med datum', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='masterprofile',
            name='name',
            field=models.CharField(verbose_name='namn', max_length=255),
        ),
    ]
