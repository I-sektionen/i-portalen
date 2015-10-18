# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0005_auto_20151005_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='iuser',
            name='email',
            field=models.EmailField(verbose_name='Email', default='noreply@i-portalen.se', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='iuser',
            name='username',
            field=models.CharField(verbose_name='LiU-ID', validators=[django.core.validators.RegexValidator('^[a-z]{4,5}\\d{3}$', 'Fel format på Liu-id. Liu-id får bara innehålla gemener (små bokstäver).')], unique=True, max_length=8),
        ),
    ]
