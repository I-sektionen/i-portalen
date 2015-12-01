# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('organisations', '0005_auto_20151012_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.TextField(null=True, verbose_name='Beskrivning', help_text='Beskrivning av organisationen',
                                   blank=True),
        ),
    ]
