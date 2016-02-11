# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0013_auto_20160101_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='modified_by',
            field=models.ForeignKey(help_text='Ändrad av.', on_delete=django.db.models.deletion.SET_NULL, verbose_name='användare', null=True, to=settings.AUTH_USER_MODEL, related_name='org_modified_by'),
        ),
        migrations.AddField(
            model_name='organisationpost',
            name='modified_by',
            field=models.ForeignKey(help_text='Ändrat av.', on_delete=django.db.models.deletion.SET_NULL, verbose_name='användare', null=True, to=settings.AUTH_USER_MODEL, related_name='org_post_modified_by'),
        ),
    ]
