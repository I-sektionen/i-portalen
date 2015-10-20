# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20151012_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='admin_group',
            field=models.ForeignKey(null=True, verbose_name='grupp som kan administrera eventet.', help_text='Utöver den användare som nu skapar eventet.', to='auth.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='deregister_delta',
            field=models.PositiveIntegerField(verbose_name='Senaste avanmälan, dagar.', help_text='Är dagar innan eventet börjar. 1 betyder att en användare kan avanmäla sig senast en dag innan eventet börjar. ', default=1),
        ),
        migrations.AlterField(
            model_name='event',
            name='lead',
            field=models.TextField(verbose_name='ingress', help_text='Max 160 characters', validators=[utils.validators.less_than_160_characters_validator]),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(verbose_name='plats', max_length=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='visible_from',
            field=models.DateTimeField(verbose_name='evenemanget är synligt ifrån'),
        ),
    ]
