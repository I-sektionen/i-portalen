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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('headline_sv', models.CharField(max_length=255)),
                ('lead_sv', models.TextField()),
                ('body_sv', models.TextField()),
                ('headline_en', models.CharField(max_length=255)),
                ('lead_en', models.TextField()),
                ('body_en', models.TextField()),
                ('visible_from', models.DateTimeField()),
                ('visible_to', models.DateTimeField()),
                ('approved', models.BooleanField()),
                ('author', models.TextField()),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name_sv', models.TextField()),
                ('name_en', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='articles.Tag'),
        ),
    ]
