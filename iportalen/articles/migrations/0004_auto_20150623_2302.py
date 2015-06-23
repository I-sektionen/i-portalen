# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='approved',
            field=models.BooleanField(verbose_name='godkänd'),
        ),
        migrations.AlterField(
            model_name='article',
            name='body_en',
            field=models.TextField(verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='article',
            name='body_sv',
            field=models.TextField(verbose_name='brödtext'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateTimeField(verbose_name='skapad', editable=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline_en',
            field=models.CharField(verbose_name='headline', max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline_sv',
            field=models.CharField(verbose_name='rubrik', max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='lead_en',
            field=models.TextField(verbose_name='lead'),
        ),
        migrations.AlterField(
            model_name='article',
            name='lead_sv',
            field=models.TextField(verbose_name='ingress'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(verbose_name='tag', to='articles.Tag'),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=models.DateTimeField(verbose_name='uppdaterad', editable=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(verbose_name='användare', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='visible_from',
            field=models.DateTimeField(verbose_name='publicera från', default=datetime.datetime(2015, 6, 23, 23, 2, 24, 318377)),
        ),
        migrations.AlterField(
            model_name='article',
            name='visible_to',
            field=models.DateTimeField(verbose_name='publicera till', default=2016),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name_en',
            field=models.CharField(verbose_name='name', max_length=255),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name_sv',
            field=models.CharField(verbose_name='namn', max_length=255),
        ),
    ]
