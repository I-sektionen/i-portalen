# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='namn', unique=True, max_length=255)),
                ('group', models.ManyToManyField(to='auth.Group', blank=True)),
            ],
            options={
                'verbose_name': 'tagg',
                'verbose_name_plural': 'taggar',
            },
        ),
    ]
