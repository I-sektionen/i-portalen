# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0029_imageattachment_otherattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageattachment',
            name='modified_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, help_text='Uppladdat av.', null=True, verbose_name='användare', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='otherattachment',
            name='modified_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, help_text='Uppladdat av.', null=True, verbose_name='användare', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
