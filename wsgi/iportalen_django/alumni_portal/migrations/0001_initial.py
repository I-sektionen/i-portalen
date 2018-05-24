# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.time
import utils.validators
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0014_auto_20160207_1236'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0003_remove_tag_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumni_Article',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('headline', models.CharField(help_text='Rubriken till artikeln', max_length=255, verbose_name='rubrik')),
                ('lead', models.TextField(help_text='Ingressen är den text som syns i nyhetsflödet. Max 160 tecken.', validators=[utils.validators.less_than_160_characters_validator], verbose_name='ingress')),
                ('body', models.TextField(help_text='Brödtext syns när en artikel visas enskilt.', verbose_name='brödtext')),
                ('visible_from', models.DateTimeField(help_text='Publiceringsdatum', default=utils.time.now, verbose_name='publicering')),
                ('visible_to', models.DateTimeField(help_text='Avpubliceringsdatum', default=utils.time.now_plus_one_month, verbose_name='avpublicering')),
                ('rejection_message', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(editable=False)),
                ('kind', models.CharField(help_text='Välj om du vill skapa en artikel eller ett event.', choices=[('a', 'Artikel'), ('e', 'Event')], max_length=1, default='a', verbose_name='Typ')),
                ('organisations', models.ManyToManyField(help_text='Om du väljer en organisation i listan du inte tillhör kommer du att tappa åtkomsten till artikeln. Håll ner Ctrl för att markera flera.', to='organisations.Organisation', verbose_name='organisationer', blank=True)),
                ('replacing', models.ForeignKey(blank=True, to='alumni_portal.Alumni_Article', null=True, default=None, on_delete=django.db.models.deletion.SET_NULL)),
                ('tags', models.ManyToManyField(help_text='Håll ner Ctrl för att markera flera.', to='tags.Tag', verbose_name='tag', blank=True)),
                ('user', models.ForeignKey(verbose_name='användare', help_text='Användaren som skrivit texten', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name_plural': 'Artiklar/Event',
                'verbose_name': 'Artikel/Event',
                'permissions': (('can_approve_article', 'Can approve article'),),
            },
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(help_text='Titel på tidningen', max_length=255, verbose_name='titel')),
                ('url', models.URLField(help_text='URL till tidningen', verbose_name='URL')),
                ('thumbnail', models.TextField(help_text='thumbnail som ska visas', default='https://www.rosegoldstudio.com/wp-content/plugins/penci-portfolio//images/no-thumbnail.jpg', verbose_name='thumbnail')),
                ('date', models.DateField(help_text='utgivningsdatum för tidningen', verbose_name='utgivningsdatum')),
            ],
            options={
                'verbose_name_plural': 'Tidningar',
                'verbose_name': 'Tidning',
            },
        ),
    ]
