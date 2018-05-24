# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0060_auto_20180521_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='Typ', max_length=1, default='a', choices=[('a', 'Artikel'), ('e', 'Event')], help_text='Välj om du vill skapa en artikel eller ett event.'),
        ),
    ]
