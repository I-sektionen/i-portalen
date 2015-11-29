# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('organisations', '0002_auto_20150711_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='contact_info',
            field=models.TextField(blank=True, null=True, verbose_name='Kontaktinformation',
                                   help_text='Kontaktinformation för organisationen'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Beskrivning',
                                   help_text='Beskrivning av organisationen'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='image',
            field=models.FileField(verbose_name='Bild', upload_to='organisations', blank=True, null=True,
                                   help_text='Bild för organisationen'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='leader',
            field=models.ForeignKey(related_name='leader', verbose_name='Ledare', blank=True,
                                    to=settings.AUTH_USER_MODEL, null=True, help_text='Ledare för organisationen'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='members',
                                         verbose_name='Medlemmar', help_text='Medlemmar i organisationen'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='name',
            field=models.CharField(unique=True, validators=[
                django.core.validators.RegexValidator('^[^/]+$', "Kan inte innehålla '/'")], max_length=255,
                                   verbose_name='Namn', help_text='Namn för organisationen'),
        ),
    ]
