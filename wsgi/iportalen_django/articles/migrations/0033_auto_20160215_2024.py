# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0032_remove_article_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(default='d', max_length=1, choices=[('d', 'Utkast'), ('b', 'väntar på godkännande'), ('r', 'Avslaget'), ('a', 'Godkänt')]),
        ),
    ]
