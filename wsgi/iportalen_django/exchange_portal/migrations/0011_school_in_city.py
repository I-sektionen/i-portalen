# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0010_remove_school_in_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='in_city',
            field=models.ForeignKey(to='exchange_portal.City', default=12),
            preserve_default=False,
        ),
    ]
