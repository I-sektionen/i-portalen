# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('organisations', '0006_auto_20151020_2223'),
        ('articles', '0011_article_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='organisations',
            field=models.ManyToManyField(to='organisations.Organisation', verbose_name='organisationer', default=None,
                                         null=True, blank=True,
                                         help_text='Organisation/organisationer som artikeln hör till'),
        ),
    ]
