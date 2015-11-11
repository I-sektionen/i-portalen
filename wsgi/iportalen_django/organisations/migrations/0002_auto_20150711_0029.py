# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='organisation_type',
            field=models.CharField(choices=[('N', 'Inte i menyn'), ('S', 'Sektionen'), ('F', 'Föreningar'), ('U', 'Utskott')], default='N', max_length=1, verbose_name='Meny', help_text='Under vilken menyrubrik ska organisationen ligga, (Gäller inte om en föräldrar organisation är vald)'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='parent_organisation',
            field=models.ForeignKey(related_name='parent', verbose_name='Föräldrar organisation', blank=True, to='organisations.Organisation', null=True, help_text='Organisation under vilken denna organisation ligger'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='image',
            field=models.FileField(blank=True, upload_to='organisations', null=True),
        ),
    ]
