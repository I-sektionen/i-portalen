# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import exchange_portal.models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_story',
            name='upload',
        ),
        migrations.AddField(
            model_name='travel_story',
            name='file',
            field=models.FileField(default=1, upload_to=exchange_portal.models._file_path),
            preserve_default=False,
        ),
    ]
