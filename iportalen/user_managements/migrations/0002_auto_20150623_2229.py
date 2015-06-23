# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iuser',
            name='bachelor_profile',
            field=models.ForeignKey(null=True, to='user_managements.BachelorProfile', blank=True),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='master_profile',
            field=models.ForeignKey(null=True, to='user_managements.MasterProfile', blank=True),
        ),
    ]
