# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0005_auto_20180424_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni_article',
            name='kind',
            field=models.TextField(verbose_name='typ', max_length=1, blank=True, default='a', choices=[('a', 'Artikel'), ('e', 'Event')], help_text='Är detta ett event eller en artikel?'),
        ),
    ]
