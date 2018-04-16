# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0011_auto_20180129_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel_story',
            name='time_abroad',
            field=models.DateField(verbose_name='', default=datetime.datetime(2018, 2, 8, 16, 25, 51, 243511, tzinfo=utc), help_text='Datum när du var utomlands'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='lead',
            field=models.TextField(verbose_name='ingress', help_text='Ingressen är den text som syns i reseberättelse'),
        ),
    ]
