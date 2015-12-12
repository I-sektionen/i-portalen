# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0023_entryasparticipant_speech_nr'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeakerList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('event',
                 models.ForeignKey(verbose_name='arrangemang', on_delete=django.db.models.deletion.SET_NULL, null=True,
                                   to='events.Event')),
                ('user',
                 models.ForeignKey(verbose_name='användare', on_delete=django.db.models.deletion.SET_NULL, null=True,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
