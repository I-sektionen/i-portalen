# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0007_auto_20180503_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni_article',
            name='kind',
            field=models.CharField(verbose_name='typ', max_length=1, default='A', choices=[('A', 'Artikel'), ('E', 'Event')], help_text='A för artikel eller E för event'),
        ),
    ]
