# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_remove_event_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='published_from',
        ),
        migrations.RemoveField(
            model_name='event',
            name='visible_to',
        ),
        migrations.AlterField(
            model_name='event',
            name='deregister_delta',
            field=models.DurationField(default=datetime.timedelta(1), verbose_name='senaste avanmälan'),
        ),
        migrations.AlterField(
            model_name='event',
            name='enable_registration',
            field=models.BooleanField(verbose_name='användare kan anmäla sig'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(verbose_name='eventets slut'),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_limit',
            field=models.IntegerField(verbose_name='maximalt antal anmälningar', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='eventets start'),
        ),
    ]
