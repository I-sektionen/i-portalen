# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('course_code', models.CharField(verbose_name='Kurskod', max_length=10)),
                ('name', models.CharField(verbose_name='Kursnamn', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('exam_code', models.CharField(verbose_name='Tentamenskod', max_length=10)),
                ('name', models.CharField(verbose_name='Tentanamn', max_length=255)),
                ('date', models.DateField()),
                ('course', models.ForeignKey(to='webgroup.Course')),
            ],
        ),
        migrations.CreateModel(
            name='ExamResult',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('amount', models.IntegerField()),
                ('exam', models.ForeignKey(to='webgroup.Exam')),
            ],
        ),
    ]
