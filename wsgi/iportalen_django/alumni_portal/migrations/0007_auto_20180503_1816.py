# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0006_alumni_article_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='typ', max_length=1, blank=True, default='Article', choices=[('Article', 'Artikel'), ('Event', 'Event')], help_text='Skriv Article för artikel eller Event för event'),
        ),
    ]
