# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('fika_penalty', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fikapenalty',
            name='paid',
        ),
        migrations.AlterField(
            model_name='fikapenalty',
            name='cost',
            field=models.FloatField(verbose_name='Kostnad', help_text='För att bokföra en inbetalning sätt ett minustecken först. ex -100'),
        ),
        migrations.AlterField(
            model_name='fikapenalty',
            name='user',
            field=models.ForeignKey(verbose_name='Medlem', to=settings.AUTH_USER_MODEL),
        ),
    ]
