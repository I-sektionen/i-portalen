# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='deadline',
            field=models.ForeignKey(default=1, verbose_name='anmälningsperiod', to='events.EntryDeadline'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='event',
            field=models.ForeignKey(default=1, verbose_name='arrangemang', to='events.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='no_show',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='användare', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entrydeadline',
            name='event',
            field=models.ForeignKey(default=1, verbose_name='arrangemang', to='events.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='användare', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
