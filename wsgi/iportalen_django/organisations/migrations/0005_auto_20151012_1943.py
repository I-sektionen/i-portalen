# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0004_auto_20151011_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.TextField(verbose_name='Beskrivning', validators=[utils.validators.less_than_200_words_validator], help_text='Beskrivning av organisationen', null=True, blank=True),
        ),
    ]
