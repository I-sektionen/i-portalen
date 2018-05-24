# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0002_auto_20180228_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magazine',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='magazine',
            name='thumbnails',
            field=models.TextField(verbose_name='thumbnail', default='https://www.rosegoldstudio.com/wp-content/plugins/penci-portfolio//images/no-thumbnail.jpg', help_text='thumbnail som ska visas'),
        ),
    ]
