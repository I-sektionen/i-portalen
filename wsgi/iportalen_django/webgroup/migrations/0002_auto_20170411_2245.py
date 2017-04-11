# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgroup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(verbose_name='Kurskod', unique=True, max_length=10),
        ),
    ]
