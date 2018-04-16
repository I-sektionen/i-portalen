# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0008_auto_20180129_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel_story',
            name='other_text',
            field=models.TextField(verbose_name='övrigt', null=True, help_text='Brödtext syns när en reseberättelse visas enskilt.'),
        ),
    ]
