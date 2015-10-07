# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('events', '0008_event_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='admin_group',
            field=models.ForeignKey(blank=True, to='auth.Group', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='deltagare', blank=True, related_name='participates_on'),
        ),
    ]
