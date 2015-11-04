# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0009_auto_20151103_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='organisation_type',
            field=models.CharField(max_length=1, verbose_name='Meny', help_text='Under vilken menyrubrik ska organisationen ligga, (Välj samma som hos föräldrar organisationen om en sådan är vald)', default='N', choices=[('N', 'Inte i menyn'), ('S', 'Sektionen'), ('F', 'Föreningar'), ('U', 'Utskott')]),
        ),
    ]
