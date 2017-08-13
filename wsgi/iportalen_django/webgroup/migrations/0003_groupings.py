# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgroup', '0002_auto_20170411_2245'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groupings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Kursnamn')),
                ('courses', models.ManyToManyField(to='webgroup.Course')),
            ],
        ),
    ]
