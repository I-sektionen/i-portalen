# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0014_auto_20160207_1236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(verbose_name='kurskod', unique=True, max_length=10)),
                ('name', models.CharField(null=True, blank=True, verbose_name='kursnamn', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'kurser',
                'verbose_name': 'kurs',
            },
        ),
        migrations.CreateModel(
            name='CourseEvaluationSettings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('evaluate_course_text', models.TextField(null=True)),
                ('mail_to_evaluator', models.TextField(help_text='Följande variabler finns att tillgå: {user} = Registrerade användarens förnamn, {period} = namnet på perioden, {year} = Året, {course} = Kursens kod och namn', null=True)),
                ('mail_to_organisation', models.TextField(help_text='Följande variabler finns att tillgå: {user} = Registrerade användarens fullständiga namn, {user_email} = Registrerade användarens epost, {period} = namnet på perioden, {year} = Året, {course} = Kursens kod och namn, {reward} = Den valda belöningen', null=True)),
                ('mail_addresses_to_organisation', models.TextField(help_text='En adress per rad.', null=True)),
                ('contact_email', models.EmailField(null=True, max_length=254)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='organisations.Organisation')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('evaluated', models.BooleanField(verbose_name='genomförd', default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='course_evaluations.Course', verbose_name='kurs')),
            ],
            options={
                'verbose_name_plural': 'kursutvärderare',
                'verbose_name': 'kursutvärderare',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('start_date', models.DateField(help_text='startdatum för perioden', verbose_name='startdatum')),
                ('end_date', models.DateField(help_text='slutdatum för perioden', verbose_name='slutdatum')),
                ('name', models.CharField(help_text='Ex, VT1', verbose_name='namn', choices=[('VT1', 'VT1'), ('VT2', 'VT2'), ('HT1', 'HT1'), ('HT2', 'HT2')], max_length=255)),
                ('courses', models.ManyToManyField(to='course_evaluations.Course', help_text='kurser att utvärdera', verbose_name='kurser')),
            ],
            options={
                'verbose_name_plural': 'läsperioder',
                'verbose_name': 'läsperiod',
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='namn', unique=True, max_length=255)),
                ('active', models.BooleanField(verbose_name='aktiv', default=False)),
            ],
            options={
                'verbose_name_plural': 'belöningar',
                'verbose_name': 'belöning',
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('year', models.IntegerField(default=2018, verbose_name='år', unique=True, choices=[(2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043), (2044, 2044), (2045, 2045), (2046, 2046), (2047, 2047), (2048, 2048), (2049, 2049), (2050, 2050), (2051, 2051), (2052, 2052), (2053, 2053), (2054, 2054), (2055, 2055), (2056, 2056), (2057, 2057), (2058, 2058), (2059, 2059), (2060, 2060), (2061, 2061), (2062, 2062), (2063, 2063), (2064, 2064), (2065, 2065), (2066, 2066), (2067, 2067)])),
                ('ht1', models.ForeignKey(verbose_name='HT1', to='course_evaluations.Period', related_name='ht1')),
                ('ht2', models.ForeignKey(verbose_name='HT2', to='course_evaluations.Period', related_name='ht2')),
                ('vt1', models.ForeignKey(verbose_name='VT1', to='course_evaluations.Period', related_name='vt1')),
                ('vt2', models.ForeignKey(verbose_name='VT2', to='course_evaluations.Period', related_name='vt2')),
            ],
            options={
                'verbose_name_plural': 'år',
                'verbose_name': 'år',
            },
        ),
        migrations.AddField(
            model_name='evaluation',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='course_evaluations.Period', verbose_name='läsperiod'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='reward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='course_evaluations.Reward', verbose_name='belönig'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='användare'),
        ),
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together=set([('course', 'period')]),
        ),
    ]
