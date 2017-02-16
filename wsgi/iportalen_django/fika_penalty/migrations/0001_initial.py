# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0014_auto_20160207_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='FikaPenalty',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('cost', models.FloatField(verbose_name='Kostnad')),
                ('date', models.DateField(verbose_name='Datum')),
                ('reason', models.TextField(null=True, blank=True, verbose_name='Anledning')),
                ('paid', models.BooleanField(default=False, verbose_name='Betald')),
                ('organisation', models.ForeignKey(to='organisations.Organisation')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
