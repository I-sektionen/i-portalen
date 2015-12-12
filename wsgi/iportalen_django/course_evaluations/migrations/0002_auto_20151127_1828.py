# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('course_evaluations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='evaluated',
            field=models.BooleanField(verbose_name='genomförd', default=False),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(verbose_name='användare', to=settings.AUTH_USER_MODEL),
        ),
    ]
