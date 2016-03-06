# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange_Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('course_code', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('is_compulsary', models.BooleanField()),
                ('technical_profile', models.CharField(choices=[('COMPUTER', 'Datateknik'), ('ENERGY', 'Energiteknik'), ('MECHANICAL', 'Maskinteknik'), ('BIO', 'Bioteknik'), ('SYSTEM', 'Systemteknik'), ('NONE', 'Ingen')], max_length=12, verbose_name='Teknisk inriktning', default='NONE')),
            ],
        ),
        migrations.CreateModel(
            name='Liu_Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('course_code', models.CharField(max_length=20)),
                ('is_compulsary', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('in_country', models.ForeignKey(to='utlandsportalen.Country')),
            ],
        ),
        migrations.AddField(
            model_name='exchange_course',
            name='corresponding_liu_course',
            field=models.ForeignKey(to='utlandsportalen.Liu_Course'),
        ),
        migrations.AddField(
            model_name='exchange_course',
            name='in_school',
            field=models.ForeignKey(to='utlandsportalen.School'),
        ),
    ]
