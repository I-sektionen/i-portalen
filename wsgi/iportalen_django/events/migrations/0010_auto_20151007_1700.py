# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0009_auto_20151006_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryAsParticipant',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Deltagare',
                'verbose_name': 'Deltagare',
            },
        ),
        migrations.CreateModel(
            name='EntryAsPreRegistered',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('no_show', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Anmälningar',
                'verbose_name': 'Anmälning',
            },
        ),
        migrations.CreateModel(
            name='EntryAsReserve',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Reserver',
                'verbose_name': 'Reserv',
            },
        ),
        migrations.RemoveField(
            model_name='entry',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='event',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='user',
        ),
        migrations.RemoveField(
            model_name='entrydeadline',
            name='event',
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'Arrangemang', 'verbose_name': 'Arrangemang',
                     'permissions': (('can_approve_article', 'Can approve article'),)},
        ),
        migrations.AddField(
            model_name='event',
            name='deregister_delta',
            field=models.DurationField(verbose_name='anmälningsslut', default=datetime.timedelta(1)),
        ),
        migrations.AddField(
            model_name='event',
            name='published_from',
            field=models.DateTimeField(blank=True, verbose_name='anmälningsstart', null=True),
        ),
        migrations.DeleteModel(
            name='Entry',
        ),
        migrations.DeleteModel(
            name='EntryDeadline',
        ),
        migrations.AddField(
            model_name='entryasreserve',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='entryasreserve',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entryaspreregistered',
            name='event',
            field=models.ForeignKey(verbose_name='arrangemang', to='events.Event'),
        ),
        migrations.AddField(
            model_name='entryaspreregistered',
            name='user',
            field=models.ForeignKey(verbose_name='användare', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entryasparticipant',
            name='event',
            field=models.ForeignKey(verbose_name='arrangemang', to='events.Event'),
        ),
        migrations.AddField(
            model_name='entryasparticipant',
            name='user',
            field=models.ForeignKey(verbose_name='användare', to=settings.AUTH_USER_MODEL),
        ),
    ]
