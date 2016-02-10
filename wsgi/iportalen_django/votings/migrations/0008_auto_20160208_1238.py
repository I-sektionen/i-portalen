# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0007_question_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='verification',
            field=models.CharField(max_length=255, null=True, help_text='Verifieringskod att ange vid omröstningen, valfritt.', blank=True, verbose_name='verifiering'),
        ),
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(max_length=1, default='d', choices=[('d', 'Utkast'), ('o', 'Öppen'), ('c', 'Stängd')]),
        ),
    ]
