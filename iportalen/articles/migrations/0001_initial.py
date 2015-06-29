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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('headline', models.CharField(max_length=255, verbose_name='rubrik')),
                ('lead', models.TextField(verbose_name='ingress')),
                ('body', models.TextField(verbose_name='brödtext')),
                ('visible_from', models.DateTimeField()),
                ('visible_to', models.DateTimeField()),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'Artiklar',
                'verbose_name': 'Artikel',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name_sv', models.CharField(max_length=255, verbose_name='namn')),
            ],
            options={
                'verbose_name_plural': 'taggar',
                'verbose_name': 'tagg',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='articles.Tag', blank=True, verbose_name='tag'),
        ),
    ]
