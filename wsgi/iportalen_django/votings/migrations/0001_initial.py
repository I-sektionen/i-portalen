# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
import utils.time


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0037_merge'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HasVoted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
                'verbose_name': 'deltagare i omröstningen',
                'verbose_name_plural': 'deltagarna i omröstningen',
            },
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='alternativ', max_length=255)),
            ],
            options={
                'verbose_name': 'alternativ',
                'verbose_name_plural': 'alternativen',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='namn', max_length=255)),
                ('body', models.TextField(verbose_name='utförlig information', help_text='Utförligare information till frågan.')),
                ('result', models.CharField(default='p', choices=[('d', 'Publik tillgång till detaljerad information om röstingen.'), ('l', 'Publik tillgång till begränsad information om röstningen.'), ('p', 'Privat åtkomst enbart för administratörer')], max_length=1)),
                ('question_status', models.CharField(default='c', choices=[('o', 'Öppen'), ('c', 'Stängd')], max_length=1)),
                ('nr_of_picks', models.IntegerField(default=1, verbose_name='Antal val en användare kan kryssa i på frågan.')),
                ('anonymous', models.BooleanField(default=True, verbose_name='namn')),
                ('modified_by', models.ForeignKey(help_text='Användaren som ändrat på frågan.', on_delete=django.db.models.deletion.SET_NULL, verbose_name='användare', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'fråga',
                'verbose_name_plural': 'frågor',
            },
        ),
        migrations.CreateModel(
            name='QuestionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('question_status', models.CharField(default='e', choices=[('e', 'Incheckade deltagare på ett event kan rösta.'), ('a', 'Alla medlemmar kan rösta')], max_length=1)),
                ('visible_from', models.DateTimeField(default=utils.time.now, verbose_name='publicering', help_text='Publiceringsdatum')),
                ('visible_to', models.DateTimeField(default=utils.time.now_plus_one_month, verbose_name='avpublicering', help_text='Avpubliceringsdatum')),
                ('event', models.ForeignKey(verbose_name='event', to='events.Event', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'frågegrupp',
                'verbose_name_plural': 'frågegrupper',
            },
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('option', models.ForeignKey(verbose_name='alternativ', to='votings.Options')),
                ('question', models.ForeignKey(verbose_name='fråga', to='votings.Question')),
                ('user', models.ForeignKey(verbose_name='användare', to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'röst',
                'verbose_name_plural': 'röster',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='question_group',
            field=models.ForeignKey(verbose_name='frågegrupp', to='votings.QuestionGroup'),
        ),
        migrations.AddField(
            model_name='options',
            name='question',
            field=models.ForeignKey(verbose_name='fråga', to='votings.Question'),
        ),
        migrations.AddField(
            model_name='hasvoted',
            name='question',
            field=models.ForeignKey(verbose_name='fråga', to='votings.Question'),
        ),
        migrations.AddField(
            model_name='hasvoted',
            name='user',
            field=models.ForeignKey(verbose_name='användare', to=settings.AUTH_USER_MODEL),
        ),
    ]
