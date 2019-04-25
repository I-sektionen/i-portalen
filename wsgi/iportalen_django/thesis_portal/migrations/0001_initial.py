# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.time
import django.db.models.deletion
from django.conf import settings
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0014_auto_20160207_1236'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thesis_Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('company', models.CharField(verbose_name='företagsnamn', max_length=255, help_text='Annonseringsföretagets namn')),
                ('headline', models.CharField(verbose_name='rubrik', max_length=255, help_text='Rubriken till annonsen')),
                ('lead', models.TextField(verbose_name='ingress', help_text='Ingressen är den text som syns i nyhetsflödet. Max 160 tecken.', validators=[utils.validators.less_than_160_characters_validator])),
                ('body', models.TextField(verbose_name='brödtext', help_text='Brödtext syns när annonsen visas enskilt.')),
                ('location', models.CharField(verbose_name='ort', max_length=64, help_text='Ort')),
                ('payed', models.BooleanField(verbose_name='betalt', default=False, help_text='Kryssa i om exjobbet är betalt')),
                ('visible_from', models.DateTimeField(verbose_name='publicering', default=utils.time.now, help_text='Publiceringsdatum')),
                ('visible_to', models.DateTimeField(verbose_name='avpublicering', default=utils.time.now_plus_one_month, help_text='Avpubliceringsdatum')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(editable=False)),
                ('organisations', models.ManyToManyField(verbose_name='organisationer', blank=True, help_text='Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln. Håll ner Ctrl för att markera flera.', to='organisations.Organisation')),
                ('user', models.ForeignKey(verbose_name='användare', null=True, help_text='Användaren som skrivit texten', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Annons',
                'verbose_name_plural': 'Annonser',
                'permissions': (('can_approve_thesis_article', 'Can approve thesis articles'),),
            },
        ),
    ]
