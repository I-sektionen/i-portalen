# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0034_auto_20160218_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='job_advert',
            field=models.BooleanField(help_text='Kryssa i om innehållet är en jobbannons', verbose_name='jobbannons', default=False),
        ),
    ]
