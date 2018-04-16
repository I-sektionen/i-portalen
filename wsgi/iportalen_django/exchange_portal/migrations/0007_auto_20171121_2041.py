# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0006_remove_travel_story_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel_story',
            name='body',
            field=models.TextField(verbose_name='brödtext', help_text='Brödtext syns när en reseberättelse visas enskilt.'),
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='headline',
            field=models.CharField(verbose_name='rubrik', max_length=255, help_text='Rubriken till reseberättelsen'),
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='lead',
            field=models.TextField(verbose_name='ingress', help_text='Ingressen är den text som syns i reseberättelse.'),
        ),
    ]
