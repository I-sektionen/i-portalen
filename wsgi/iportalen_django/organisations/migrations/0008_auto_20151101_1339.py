# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0007_auto_20151027_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='contact_info',
            field=models.EmailField(help_text='Kontaktinformation för organisationen', null=True, blank=True, verbose_name='Mejlkontakt', max_length=254),
        ),
    ]
