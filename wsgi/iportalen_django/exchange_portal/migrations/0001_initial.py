# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Stad',
                'verbose_name_plural': 'Städer',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('course_code', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('technical_profile', models.CharField(verbose_name='Teknisk inriktning', max_length=12, default='NONE', choices=[('Datateknik', 'Datateknik'), ('Energiteknik', 'Energiteknik'), ('Maskinteknik', 'Maskinteknik'), ('Bioteknik', 'Bioteknik'), ('Systemteknik', 'Systemteknik'), ('Ingen', 'Ingen')])),
            ],
            options={
                'verbose_name': 'Utlandskurs',
                'verbose_name_plural': 'Utlandskurser',
            },
        ),
        migrations.CreateModel(
            name='Liu_Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('in_city', models.ForeignKey(to='exchange_portal.City')),
            ],
            options={
                'verbose_name': 'Skola',
                'verbose_name_plural': 'Skolor',
            },
        ),
        migrations.CreateModel(
            name='Travel_Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('upload', models.FileField(upload_to='travel_stories/%Y%m%d/')),
                ('added_by_user', models.CharField(verbose_name='liu-id', max_length=10)),
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
        migrations.AddField(
            model_name='city',
            name='in_country',
            field=models.ForeignKey(to='exchange_portal.Country'),
        ),
    ]
