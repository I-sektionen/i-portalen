# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='IUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[a-zA-Z]{5}\\d{3}$')], verbose_name='LiU-ID', unique=True, max_length=8)),
                ('first_name', models.CharField(null=True, verbose_name='förnamn', max_length=50, blank=True)),
                ('last_name', models.CharField(null=True, verbose_name='efternamn', max_length=50, blank=True)),
                ('date_joined', models.DateTimeField(verbose_name='gick med datum', auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('p_nr', models.CharField(null=True, verbose_name='personnummer', max_length=255, blank=True)),
                ('address', models.CharField(null=True, verbose_name='adress', max_length=255, blank=True)),
                ('zip_code', models.CharField(null=True, verbose_name='postnummer', max_length=255, blank=True)),
                ('city', models.CharField(null=True, verbose_name='ort', max_length=255, blank=True)),
                ('gender', models.CharField(null=True, verbose_name='kön', max_length=255, blank=True)),
                ('allergies', models.TextField(verbose_name='allergier', null=True, blank=True)),
                ('start_year', models.IntegerField(choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], verbose_name='start år', default=2015)),
                ('expected_exam_year', models.IntegerField(choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], verbose_name='förväntat examens år', default=2020)),
            ],
            options={
                'verbose_name': 'användare',
                'verbose_name_plural': 'användare',
            },
        ),
        migrations.CreateModel(
            name='BachelorProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='namn', max_length=255)),
            ],
            options={
                'verbose_name': 'kandidatprofil',
                'verbose_name_plural': 'kandidatprofiler',
            },
        ),
        migrations.CreateModel(
            name='MasterProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='namn', max_length=255)),
            ],
            options={
                'verbose_name': 'masterprofil',
                'verbose_name_plural': 'masterprofiler',
            },
        ),
        migrations.AddField(
            model_name='iuser',
            name='bachelor_profile',
            field=models.ForeignKey(to='user_managements.BachelorProfile', verbose_name='kandidatprofil', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='iuser',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', verbose_name='groups', related_name='user_set', related_query_name='user', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        ),
        migrations.AddField(
            model_name='iuser',
            name='master_profile',
            field=models.ForeignKey(to='user_managements.MasterProfile', verbose_name='masterprofil', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='iuser',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', related_name='user_set', related_query_name='user', blank=True, help_text='Specific permissions for this user.'),
        ),
    ]
