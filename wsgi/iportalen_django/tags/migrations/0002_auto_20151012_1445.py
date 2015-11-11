# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True, validators=[django.core.validators.RegexValidator('^[^/]+$', "Kan inte innehålla '/'")], verbose_name='namn', max_length=255),
        ),
    ]
