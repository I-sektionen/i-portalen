# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0021_auto_20151103_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='article',
            name='draft',
        ),
        migrations.AddField(
            model_name='article',
            name='rejection_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(
                choices=[('d', 'utkast'), ('b', 'väntar på godkännande'), ('r', 'Avslaget'), ('a', 'Godkännt')],
                max_length=1, default='d'),
        ),
    ]
