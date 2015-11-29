# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0018_auto_20151101_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='approved',
        ),
        migrations.AddField(
            model_name='event',
            name='rejection_message',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(max_length=1, default='d',
                                   choices=[('d', 'utkast'), ('b', 'väntar på godkännande'), ('r', 'Avslaget'),
                                            ('a', 'Godkännt')]),
        ),
    ]
