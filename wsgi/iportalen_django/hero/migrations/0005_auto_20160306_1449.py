# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import hero.models


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0004_auto_20160302_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='file',
            field=models.FileField(upload_to=hero.models._file_path, help_text='Filstorleken bör inte vara större än 0,5mb. Bilden bör vara ungefär 2500*350 för bästa utseende.', verbose_name='Hero'),
        ),
    ]
