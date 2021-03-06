# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0011_organisationpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='organisation_type',
            field=models.CharField(choices=[('N', 'Inte i menyn'), ('S', 'Sektionen'), ('F', 'Föreningar')], default='N', help_text='Under vilken menyrubrik ska organisationen ligga, (Välj samma som hos föräldrar organisationen om en sådan är vald)', max_length=1, null=True, verbose_name='Meny'),
        ),
    ]
