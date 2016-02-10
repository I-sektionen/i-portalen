# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('votings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'röster',
                'verbose_name': 'röst',
            },
        ),
        migrations.RenameModel(
            old_name='Options',
            new_name='Option',
        ),
        migrations.RemoveField(
            model_name='votes',
            name='option',
        ),
        migrations.RemoveField(
            model_name='votes',
            name='question',
        ),
        migrations.RemoveField(
            model_name='votes',
            name='user',
        ),
        migrations.DeleteModel(
            name='Votes',
        ),
        migrations.AddField(
            model_name='vote',
            name='option',
            field=models.ForeignKey(verbose_name='alternativ', to='votings.Option'),
        ),
        migrations.AddField(
            model_name='vote',
            name='question',
            field=models.ForeignKey(verbose_name='fråga', to='votings.Question'),
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(blank=True, null=True, verbose_name='användare', to=settings.AUTH_USER_MODEL),
        ),
    ]
