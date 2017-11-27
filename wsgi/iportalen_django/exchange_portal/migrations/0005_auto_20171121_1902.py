# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_remove_tag_group'),
        ('exchange_portal', '0004_auto_20170307_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_story',
            name='file',
        ),
        migrations.AddField(
            model_name='travel_story',
            name='body',
            field=models.TextField(verbose_name='brödtext', default=datetime.datetime(2017, 11, 21, 18, 2, 19, 883012, tzinfo=utc), help_text='Brödtext syns när en artikel visas enskilt.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='headline',
            field=models.CharField(verbose_name='rubrik', max_length=255, default=datetime.datetime(2017, 11, 21, 18, 2, 36, 462866, tzinfo=utc), help_text='Rubriken till artikeln'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='lead',
            field=models.TextField(verbose_name='ingress', default=1, help_text='Ingressen är den text som syns i nyhetsflödet. Max 160 tecken.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='tags',
            field=models.ManyToManyField(verbose_name='tag', blank=True, help_text='Håll ner Ctrl för att markera flera.', to='tags.Tag'),
        ),
        migrations.AlterField(
            model_name='liu_course',
            name='is_compulsary',
            field=models.BooleanField(default=False),
        ),
    ]
