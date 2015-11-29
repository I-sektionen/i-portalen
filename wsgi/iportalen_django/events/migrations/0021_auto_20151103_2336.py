# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0020_auto_20151103_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entryasparticipant',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='arrangemang', null=True,
                                    to='events.Event'),
        ),
        migrations.AlterField(
            model_name='entryasparticipant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='användare', null=True,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entryaspreregistered',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='arrangemang', null=True,
                                    to='events.Event'),
        ),
        migrations.AlterField(
            model_name='entryaspreregistered',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='användare', null=True,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entryasreserve',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='events.Event'),
        ),
        migrations.AlterField(
            model_name='entryasreserve',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='användare', null=True,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
