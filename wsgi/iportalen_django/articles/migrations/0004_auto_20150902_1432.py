# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20150711_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(verbose_name='brödtext', help_text='Brödtext som syns efter att ha klickat på läs mer.'),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline',
            field=models.CharField(verbose_name='rubrik', max_length=255, help_text='Rubriken till Artikeln'),
        ),
        migrations.AlterField(
            model_name='article',
            name='lead',
            field=models.TextField(verbose_name='ingress', help_text='Ingress som syns utan att klicka på artikeln.'),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(verbose_name='användare', to=settings.AUTH_USER_MODEL, help_text='Skribent av texten'),
        ),
        migrations.AlterField(
            model_name='article',
            name='visible_from',
            field=models.DateTimeField(verbose_name='publicering', help_text='Datum för publicering'),
        ),
        migrations.AlterField(
            model_name='article',
            name='visible_to',
            field=models.DateTimeField(verbose_name='avpublicering', help_text='Datum för avpublicering.'),
        ),
    ]
