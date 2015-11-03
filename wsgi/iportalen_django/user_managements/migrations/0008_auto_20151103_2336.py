# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0007_iuser_is_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iuser',
            name='bachelor_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='user_managements.BachelorProfile', verbose_name='kandidatprofil', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='master_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='user_managements.MasterProfile', verbose_name='masterprofil', null=True, blank=True),
        ),
    ]
