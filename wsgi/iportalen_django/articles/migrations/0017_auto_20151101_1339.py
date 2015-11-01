# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_auto_20151027_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(help_text='Skribent av texten visas bara om ingen organisation valts.', null=True, blank=True, verbose_name='skribent', max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='organisations',
            field=models.ManyToManyField(default=None, help_text='Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln.', blank=True, verbose_name='organisationer', to='organisations.Organisation'),
        ),
    ]
