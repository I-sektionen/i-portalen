# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazine',
            name='thumbnail',
            field=models.TextField(verbose_name='thumbnails', default='https://www.rosegoldstudio.com/wp-content/plugins/penci-portfolio//images/no-thumbnail.jpg', help_text='thumbnail som ska visas'),
        ),
    ]
