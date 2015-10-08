# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0003_auto_20151005_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='parent_organisation',
            field=models.ForeignKey(null=True, related_name='parent', blank=True, to='organisations.Organisation'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(unique=True, validators=[django.core.validators.RegexValidator('^[^/]+$', "Kan inte innehålla '/'")], max_length=255),
        ),

    ]
