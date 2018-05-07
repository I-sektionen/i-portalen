# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0014_auto_20160207_1236'),
        ('alumni_portal', '0004_auto_20180228_1830'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='magazine',
            options={'verbose_name': 'Tidning', 'verbose_name_plural': 'Tidningar'},
        ),
        migrations.AddField(
            model_name='alumni_article',
            name='organisations',
            field=models.ManyToManyField(verbose_name='organisationer', blank=True, help_text='Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln. Håll ner Ctrl för att markera flera.', to='organisations.Organisation'),
        ),
    ]
