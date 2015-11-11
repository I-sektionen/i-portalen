# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_auto_20151103_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.AlterField(
            model_name='article',
            name='organisations',
            field=models.ManyToManyField(to='organisations.Organisation', help_text='Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln.', verbose_name='organisationer'),
        ),
    ]
