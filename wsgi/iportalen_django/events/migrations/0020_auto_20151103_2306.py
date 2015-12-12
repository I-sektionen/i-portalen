# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0019_auto_20151102_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='admin_group',
        ),
        migrations.AlterField(
            model_name='event',
            name='organisations',
            field=models.ManyToManyField(default=None, to='organisations.Organisation', verbose_name='arrangör',
                                         help_text='Organisation(er) som arrangerar evenemanget. Medlemmar i dessa kan '
                                                   'senare ändra eventet.',
                                         blank=True),
        ),
    ]
