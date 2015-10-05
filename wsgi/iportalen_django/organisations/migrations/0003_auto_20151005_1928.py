# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0002_auto_20150711_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='organisation_type',
            field=models.CharField(max_length=1, choices=[('N', 'Inte i menyn'), ('S', 'Sektionen'), ('F', 'Föreningar'), ('U', 'Utskott')], default='N'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='leader',
            field=models.ForeignKey(blank=True, related_name='leader', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
