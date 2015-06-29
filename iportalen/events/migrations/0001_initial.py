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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('registered_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Anmälningar',
                'verbose_name': 'Anmälning',
            },
        ),
        migrations.CreateModel(
            name='EntryDeadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description_sv', models.TextField(verbose_name='beskrivning')),
                ('entry_from', models.DateTimeField(verbose_name='anmälningsstart')),
                ('entry_to', models.DateTimeField(verbose_name='anmälningsslut')),
                ('enable_unregistration', models.BooleanField(verbose_name='kan avanmäla sig')),
            ],
            options={
                'verbose_name_plural': 'Anmälningsperioder',
                'verbose_name': 'Anmälningsperiod',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('article_ptr', models.OneToOneField(auto_created=True, parent_link=True, serialize=False, to='articles.Article', primary_key=True)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('end', models.DateTimeField(verbose_name='slut')),
                ('enable_registration', models.BooleanField(verbose_name='kan anmäla sig')),
                ('registration_limit', models.IntegerField(verbose_name='max antal anmälningar')),
            ],
            options={
                'verbose_name_plural': 'Arrangemanger',
                'verbose_name': 'Arrangemang',
            },
            bases=('articles.article',),
        ),
        migrations.AddField(
            model_name='entrydeadline',
            name='event',
            field=models.ForeignKey(verbose_name='arrangemang', to='events.Event'),
        ),
        migrations.AddField(
            model_name='entry',
            name='deadline',
            field=models.ForeignKey(verbose_name='anmälningsperiod', to='events.EntryDeadline'),
        ),
        migrations.AddField(
            model_name='entry',
            name='event',
            field=models.ForeignKey(verbose_name='arrangemang', to='events.Event'),
        ),
    ]
