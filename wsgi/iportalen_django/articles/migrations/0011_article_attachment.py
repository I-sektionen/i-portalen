# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0010_auto_20151016_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='attachment',
            field=models.FileField(null=True, verbose_name='Bifogad fil', help_text='Bifogad fil för artikel',
                                   blank=True, upload_to='article_attachments'),
        ),
    ]
