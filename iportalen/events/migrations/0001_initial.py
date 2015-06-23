# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_remove_article_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('registered_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EntryDeadline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('description_sv', models.TextField()),
                ('description_en', models.TextField()),
                ('entry_from', models.DateTimeField()),
                ('entry_to', models.DateTimeField()),
                ('enable_unregistration', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('article_ptr', models.OneToOneField(auto_created=True, to='articles.Article', primary_key=True, parent_link=True, serialize=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('enable_registration', models.BooleanField()),
                ('registration_limit', models.IntegerField()),
            ],
            bases=('articles.article',),
        ),
        migrations.AddField(
            model_name='entrydeadline',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='entry',
            name='deadline',
            field=models.ForeignKey(to='events.EntryDeadline'),
        ),
        migrations.AddField(
            model_name='entry',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
    ]
