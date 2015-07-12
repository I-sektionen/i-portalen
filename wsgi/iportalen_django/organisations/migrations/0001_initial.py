# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('contact_info', models.TextField(null=True, blank=True)),
                ('image', models.FileField(upload_to='organisations')),
                ('leader', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='leader')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='members')),
            ],
        ),
    ]
