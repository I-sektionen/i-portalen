# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0040_auto_20160213_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeakerList',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('first', models.NullBooleanField(default=None)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='events.Event', null=True, verbose_name='arrangemang')),
                ('next_speaker', models.ForeignKey(default=None, blank=True, to='speaker_list.SpeakerList', on_delete=django.db.models.deletion.SET_NULL, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True, verbose_name='användare')),
            ],
        ),
    ]
