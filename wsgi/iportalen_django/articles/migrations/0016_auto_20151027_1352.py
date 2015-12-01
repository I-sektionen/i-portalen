# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0015_auto_20151021_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='organisations',
            field=models.ManyToManyField(blank=True, help_text='Organisation/organisationer som artikeln hör till.',
                                         default=None, to='organisations.Organisation', verbose_name='organisationer'),
        ),
    ]
