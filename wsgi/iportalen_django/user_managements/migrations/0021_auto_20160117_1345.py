# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0020_iuser_must_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='iuser',
            name='phone',
            field=models.CharField(max_length=255, null=True, verbose_name='Telefon', blank=True),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='bachelor_profile',
            field=models.ForeignKey(help_text='Välj Ej valt om du inte har valt kandidatprofil.', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='kandidatprofil', to='user_managements.BachelorProfile'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='master_profile',
            field=models.ForeignKey(help_text='Välj Ej valt om du inte har valt kandidatprofil.', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='masterprofil', to='user_managements.MasterProfile'),
        ),
    ]
