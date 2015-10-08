# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0004_auto_20151005_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='contact_info',
            field=models.TextField(blank=True, verbose_name='Kontaktinformation', help_text='Kontaktinformation för organisationen', null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beskrivning', help_text='Beskrivning av organisationen', null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='image',
            field=models.FileField(blank=True, help_text='Bild för organisationen', upload_to='organisations', verbose_name='Bild', null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='leader',
            field=models.ForeignKey(blank=True, help_text='Ledare för organisationen', to=settings.AUTH_USER_MODEL, verbose_name='Ledare', related_name='leader', null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='members',
            field=models.ManyToManyField(blank=True, verbose_name='Medlemmar', help_text='Medlemmar i organisationen', to=settings.AUTH_USER_MODEL, related_name='members'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[^/]+$', "Kan inte innehålla '/'")], verbose_name='Namn', help_text='Namn för organisationen', unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='organisation_type',
            field=models.CharField(verbose_name='Meny', help_text='Under vilken menyrubrik ska organisationen ligga, (Gäller inte om en föräldrar organisation är vald)', choices=[('N', 'Inte i menyn'), ('S', 'Sektionen'), ('F', 'Föreningar'), ('U', 'Utskott')], max_length=1, default='N'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='parent_organisation',
            field=models.ForeignKey(blank=True, help_text='Organisation under vilken denna organisation ligger', to='organisations.Organisation', verbose_name='Föräldrar organisation', related_name='parent', null=True),
        ),
    ]
