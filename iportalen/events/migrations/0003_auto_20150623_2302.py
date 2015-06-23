# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_entry_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='deadline',
            field=models.ForeignKey(verbose_name='anmälningsperiod', to='events.EntryDeadline'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='event',
            field=models.ForeignKey(verbose_name='arrangemang', to='events.Event'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='registered_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(verbose_name='användare', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entrydeadline',
            name='description_en',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='entrydeadline',
            name='description_sv',
            field=models.TextField(verbose_name='beskrivning'),
        ),
        migrations.AlterField(
            model_name='entrydeadline',
            name='enable_unregistration',
            field=models.BooleanField(verbose_name='kan avanmäla sig'),
        ),
        migrations.AlterField(
            model_name='entrydeadline',
            name='entry_from',
            field=models.DateTimeField(verbose_name='anmälningsstart'),
        ),
        migrations.AlterField(
            model_name='entrydeadline',
            name='entry_to',
            field=models.DateTimeField(verbose_name='anmälningsslut'),
        ),
        migrations.AlterField(
            model_name='entrydeadline',
            name='event',
            field=models.ForeignKey(verbose_name='arrangemang', to='events.Event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='enable_registration',
            field=models.BooleanField(verbose_name='kan anmäla sig'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(verbose_name='slut'),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_limit',
            field=models.IntegerField(verbose_name='max antal anmälningar'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='start'),
        ),
    ]
