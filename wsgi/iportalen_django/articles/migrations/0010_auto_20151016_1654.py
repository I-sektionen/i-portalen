# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
import datetime
import utils.time
import utils.validators


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0009_article_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(help_text='Brödtext syns när en artikel visas enskilt.', verbose_name='brödtext'),
        ),
        migrations.AlterField(
            model_name='article',
            name='draft',
            field=models.BooleanField(help_text='Sparar utan att publicera', verbose_name='utkast', default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='headline',
            field=models.CharField(max_length=255, help_text='Rubriken till artikeln', verbose_name='rubrik'),
        ),
        migrations.AlterField(
            model_name='article',
            name='lead',
            field=models.TextField(validators=[utils.validators.less_than_160_characters_validator],
                                   help_text='Ingressen är den text som syns i nyhetsflödet. Max 160 tecken.',
                                   verbose_name='ingress'),
        ),
        migrations.AlterField(
            model_name='article',
            name='visible_from',
            field=models.DateTimeField(help_text='Publiceringsdatum', verbose_name='publicering',
                                       default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='article',
            name='visible_to',
            field=models.DateTimeField(help_text='Avpubliceringsdatum', verbose_name='avpublicering',
                                       default=utils.time.now_plus_one_month),
        ),
    ]
