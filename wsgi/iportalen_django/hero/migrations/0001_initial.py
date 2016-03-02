# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hero.models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('file', models.FileField(verbose_name='Hero', upload_to=hero.models._file_path)),
                ('file_name', models.CharField(blank=True, max_length=300)),
                ('modified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, help_text='Uppladdat av.', verbose_name='användare', null=True)),
            ],
            options={
                'verbose_name': 'Hero',
                'verbose_name_plural': 'Herosarna',
            },
        ),
    ]
