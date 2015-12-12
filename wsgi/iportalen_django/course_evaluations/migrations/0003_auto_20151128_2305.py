# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_evaluations', '0002_auto_20151127_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='name',
            field=models.CharField(max_length=255, help_text='Ex, 2016 VT1', verbose_name='namn'),
        ),
    ]
