# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('code', models.CharField(verbose_name='kurskod', max_length=10, unique=True)),
                ('name', models.CharField(verbose_name='kursnamn', max_length=255, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'kurs',
                'verbose_name_plural': 'kurser',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('course', models.ForeignKey(to='course_evaluations.Course', verbose_name='kurs', on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
            options={
                'verbose_name': 'kursutvärderare',
                'verbose_name_plural': 'kursutvärderare',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('start_date', models.DateTimeField(verbose_name='startdatum', help_text='startdatum för perioden')),
                ('end_date', models.DateTimeField(verbose_name='slutdatum', help_text='slutdatum för perioden')),
                ('name', models.CharField(verbose_name='namn', max_length=255, help_text='Ex, VT1 2016')),
                ('courses', models.ManyToManyField(verbose_name='kurser', help_text='kurser att utvärdera', to='course_evaluations.Course')),
            ],
            options={
                'verbose_name': 'läsperiod',
                'verbose_name_plural': 'läsperioder',
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='belöning', max_length=255)),
            ],
            options={
                'verbose_name': 'belöning',
                'verbose_name_plural': 'belöningar',
            },
        ),
        migrations.AddField(
            model_name='evaluation',
            name='period',
            field=models.ForeignKey(to='course_evaluations.Period', verbose_name='läsperiod', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='reward',
            field=models.ForeignKey(to='course_evaluations.Reward', verbose_name='belönig', on_delete=django.db.models.deletion.SET_NULL, null=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(verbose_name='kurs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together=set([('course', 'period')]),
        ),
    ]
