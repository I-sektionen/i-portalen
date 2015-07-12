# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('registered_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Anmälning',
                'verbose_name_plural': 'Anmälningar',
            },
        ),
        migrations.CreateModel(
            name='EntryDeadline',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('description_sv', models.TextField(verbose_name='beskrivning')),
                ('entry_from', models.DateTimeField(verbose_name='anmälningsstart')),
                ('entry_to', models.DateTimeField(verbose_name='anmälningsslut')),
                ('enable_unregistration', models.BooleanField(verbose_name='kan avanmäla sig')),
            ],
            options={
                'verbose_name': 'Anmälningsperiod',
                'verbose_name_plural': 'Anmälningsperioder',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('headline', models.CharField(verbose_name='rubrik', max_length=255)),
                ('lead', models.TextField(verbose_name='ingress')),
                ('body', models.TextField(verbose_name='brödtext')),
                ('visible_from', models.DateTimeField()),
                ('visible_to', models.DateTimeField()),
                ('approved', models.BooleanField(verbose_name='godkänd', default=False)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(editable=False)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('end', models.DateTimeField(verbose_name='slut')),
                ('enable_registration', models.BooleanField(verbose_name='kan anmäla sig')),
                ('registration_limit', models.IntegerField(verbose_name='max antal anmälningar')),
                ('tags', models.ManyToManyField(to='articles.Tag', verbose_name='tag', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Arrangemanger',
                'verbose_name': 'Arrangemang',
                'permissions': (('can_approve_article', 'Can approve article'),),
            },
        ),
    ]
