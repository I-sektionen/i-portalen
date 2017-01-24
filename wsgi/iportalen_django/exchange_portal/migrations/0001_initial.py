# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Land',
                'verbose_name_plural': 'Länder',
            },
        ),
        migrations.CreateModel(
            name='Exchange_Course',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('course_code', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('technical_profile', models.CharField(max_length=12, verbose_name='Teknisk inriktning', default='NONE', choices=[('Datateknik', 'Datateknik'), ('Energiteknik', 'Energiteknik'), ('Maskinteknik', 'Maskinteknik'), ('Bioteknik', 'Bioteknik'), ('Systemteknik', 'Systemteknik'), ('Ingen', 'Ingen')])),
            ],
            options={
                'verbose_name': 'Utlandskurs',
                'verbose_name_plural': 'Utlandskurser',
            },
        ),
        migrations.CreateModel(
            name='IUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('username', models.CharField(verbose_name='LiU-ID', unique=True, validators=[django.core.validators.RegexValidator('^[a-z]{4,5}\\d{3}$', 'Fel format på Liu-id. Liu-id får bara innehålla gemener (små bokstäver).')], max_length=8)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('first_name', models.CharField(null=True, max_length=50, blank=True, verbose_name='förnamn')),
                ('last_name', models.CharField(null=True, max_length=50, blank=True, verbose_name='efternamn')),
            ],
            options={
                'verbose_name': 'användare',
                'verbose_name_plural': 'användare',
            },
        ),
        migrations.CreateModel(
            name='Liu_Course',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('course_code', models.CharField(max_length=20)),
                ('is_compulsary', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Liukurs',
                'verbose_name_plural': 'Liukurser',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('in_country', models.ForeignKey(to='exchange_portal.Country')),
            ],
            options={
                'verbose_name': 'Skola',
                'verbose_name_plural': 'Skolor',
            },
        ),
        migrations.CreateModel(
            name='Travel_Story',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('upload', models.FileField(upload_to='travler_stories/%Y%m%d/')),
                ('added_by_user', models.CharField(max_length=10, verbose_name='liu-id')),
                ('about_school', models.ForeignKey(to='exchange_portal.School')),
            ],
            options={
                'verbose_name': 'Reseberättelse',
                'verbose_name_plural': 'Reseberättelser',
            },
        ),
        migrations.AddField(
            model_name='exchange_course',
            name='corresponding_liu_course',
            field=models.ForeignKey(to='exchange_portal.Liu_Course'),
        ),
        migrations.AddField(
            model_name='exchange_course',
            name='in_school',
            field=models.ForeignKey(to='exchange_portal.School'),
        ),
    ]
