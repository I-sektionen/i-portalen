# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('organisations', '0008_auto_20151101_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='group',
            field=models.ForeignKey(related_name='group', to='auth.Group', help_text='Grupp knuten till organisationen',
                                    verbose_name='Grupp', null=True, blank=True,
                                    on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='leader',
            field=models.ForeignKey(related_name='leader', to=settings.AUTH_USER_MODEL,
                                    help_text='Ledare för organisationen', verbose_name='Ledare', null=True, blank=True,
                                    on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='parent_organisation',
            field=models.ForeignKey(related_name='parent', to='organisations.Organisation',
                                    help_text='Organisation under vilken denna organisation ligger',
                                    verbose_name='Föräldrar organisation', null=True, blank=True,
                                    on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
