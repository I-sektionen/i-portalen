# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import utils.validators
import utils.time


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_remove_tag_group'),
        ('organisations', '0014_auto_20160207_1236'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alumni_portal', '0058_auto_20180521_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumni_Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('headline', models.CharField(verbose_name='rubrik', max_length=255, help_text='Rubriken till artikeln')),
                ('lead', models.TextField(verbose_name='ingress', help_text='Ingressen är den text som syns i nyhetsflödet. Max 160 tecken.', validators=[utils.validators.less_than_160_characters_validator])),
                ('body', models.TextField(verbose_name='brödtext', help_text='Brödtext syns när en artikel visas enskilt.')),
                ('visible_from', models.DateTimeField(verbose_name='publicering', default=utils.time.now, help_text='Publiceringsdatum')),
                ('visible_to', models.DateTimeField(verbose_name='avpublicering', default=utils.time.now_plus_one_month, help_text='Avpubliceringsdatum')),
                ('rejection_message', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(editable=False)),
                ('kind', models.CharField(verbose_name='Typ', max_length=1, default='a', choices=[('a', 'Artikel'), ('e', 'Event')])),
                ('organisations', models.ManyToManyField(verbose_name='organisationer', blank=True, help_text='Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln. Håll ner Ctrl för att markera flera.', to='organisations.Organisation')),
                ('replacing', models.ForeignKey(blank=True, null=True, default=None, on_delete=django.db.models.deletion.SET_NULL, to='alumni_portal.Alumni_Article')),
                ('tags', models.ManyToManyField(verbose_name='tag', blank=True, help_text='Håll ner Ctrl för att markera flera.', to='tags.Tag')),
                ('user', models.ForeignKey(verbose_name='användare', null=True, help_text='Användaren som skrivit texten', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Artikel',
                'verbose_name_plural': 'Artiklar',
                'permissions': (('can_approve_article', 'Can approve article'),),
            },
        ),
    ]