# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0014_auto_20160207_1236'),
        ('votings', '0004_questiongroup_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiongroup',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='skapare'),
        ),
        migrations.AddField(
            model_name='questiongroup',
            name='organisations',
            field=models.ManyToManyField(default=None, blank=True, to='organisations.Organisation', verbose_name='administrerar', help_text='Organisation(er) som administrerar frågeguppen, Håll ner Ctrl för att markera flera.'),
        ),
    ]
