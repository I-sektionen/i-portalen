# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('organisations', '0003_auto_20151008_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='members',
        ),
        migrations.AddField(
            model_name='organisation',
            name='group',
            field=models.ForeignKey(verbose_name='Grupp', help_text='Grupp knuten till organisationen', blank=True, to='auth.Group', related_name='group', null=True),
        ),
    ]
