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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator('^[a-zA-Z]{5}\\d{3}$')], verbose_name='LiU-ID', unique=True)),
                ('first_name', models.CharField(null=True, max_length=50, blank=True, verbose_name='förnamn')),
                ('last_name', models.CharField(null=True, max_length=50, blank=True, verbose_name='efternamn')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='gick med datum')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('p_nr', models.CharField(null=True, max_length=255, blank=True, verbose_name='personnummer')),
                ('address', models.CharField(null=True, max_length=255, blank=True, verbose_name='adress')),
                ('zip_code', models.CharField(null=True, max_length=255, blank=True, verbose_name='postnummer')),
                ('city', models.CharField(null=True, max_length=255, blank=True, verbose_name='ort')),
                ('gender', models.CharField(null=True, max_length=255, blank=True, verbose_name='kön')),
                ('allergies', models.TextField(null=True, blank=True, verbose_name='allergier')),
                ('start_year', models.IntegerField(choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], verbose_name='start år', default=2015)),
                ('expected_exam_year', models.IntegerField(choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], verbose_name='förväntat examens år', default=2020)),
            ],
            options={
                'verbose_name_plural': 'användare',
                'verbose_name': 'användare',
            },
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('approved', models.BooleanField(verbose_name='godkänd')),
            ],
        ),
        migrations.CreateModel(
            name='BachelorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='namn')),
            ],
            options={
                'verbose_name_plural': 'kandidatprofiler',
                'verbose_name': 'kandidatprofil',
            },
        ),
        migrations.CreateModel(
            name='MasterProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='namn')),
            ],
            options={
                'verbose_name_plural': 'masterprofiler',
                'verbose_name': 'masterprofil',
            },
        ),
        migrations.AddField(
            model_name='iuser',
            name='bachelor_profile',
            field=models.ForeignKey(null=True, to='user_managements.BachelorProfile', verbose_name='kandidatprofil', blank=True),
        ),
        migrations.AddField(
            model_name='iuser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', related_name='user_set', related_query_name='user', verbose_name='groups', blank=True),
        ),
        migrations.AddField(
            model_name='iuser',
            name='master_profile',
            field=models.ForeignKey(null=True, to='user_managements.MasterProfile', verbose_name='masterprofil', blank=True),
        ),
        migrations.AddField(
            model_name='iuser',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', related_name='user_set', related_query_name='user', verbose_name='user permissions', blank=True),
        ),
    ]
