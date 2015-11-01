# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20151021_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='body',
            field=models.TextField(help_text='Beskrivning av eventet', verbose_name='beskrivning'),
        ),
        migrations.AlterField(
            model_name='event',
            name='deregister_delta',
            field=models.PositiveIntegerField(help_text='Sista dag för avanmälan i antal dagar innan eventet', verbose_name='Sista dag för använmälan', default=1),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(help_text='När slutar arrangemanget?', verbose_name='sluttid'),
        ),
        migrations.AlterField(
            model_name='event',
            name='headline',
            field=models.CharField(help_text="Ge ditt evenemang en titel, till exempel 'Excelutbildning med Knowit'", verbose_name='arrangemangets namn', max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='lead',
            field=models.TextField(help_text="Ge en kort beskrivning av ditt event. Max 160 tecken. Tex. 'Få cellsynt kompetens med Knowit!'", verbose_name='kort beskrivning', validators=[utils.validators.less_than_160_characters_validator]),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(help_text='Plats för eventet tex. C1 eller Märkesbacken', verbose_name='plats', max_length=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_limit',
            field=models.PositiveIntegerField(blank=True, help_text='Hur många kan anmäla sig?', verbose_name='antal platser', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(help_text='När startar arrangemanget?', verbose_name='starttid'),
        ),
        migrations.AlterField(
            model_name='event',
            name='visible_from',
            field=models.DateTimeField(verbose_name='Datum för publicering'),
        ),
    ]
