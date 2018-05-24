# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_portal', '0003_auto_20180228_1828'),
    ]

    operations = [
        migrations.RenameField(
            model_name='magazine',
            old_name='thumbnails',
            new_name='thumbnail',
        ),
    ]
