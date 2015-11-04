# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_auto_20151103_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='replacing',
            field=models.ForeignKey(to='articles.Article', on_delete=django.db.models.deletion.SET_NULL, null=True, default=None, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, help_text='Användaren som skrivit texten', verbose_name='användare', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
