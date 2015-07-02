# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
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
            ],
            options={
                'verbose_name_plural': 'Artiklar',
                'verbose_name': 'Artikel',
                'permissions': (('can_approve_article', 'Can approve article'),),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name_sv', models.CharField(verbose_name='namn', max_length=255)),
            ],
            options={
                'verbose_name': 'tagg',
                'verbose_name_plural': 'taggar',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='articles.Tag', verbose_name='tag', blank=True),
        ),
    ]
