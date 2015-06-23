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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[a-zA-Z]{5}\\d{3}$')], verbose_name='LiU-ID', max_length=8, unique=True)),
                ('first_name', models.CharField(null=True, max_length=50, blank=True)),
                ('last_name', models.CharField(null=True, max_length=50, blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('p_nr', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('allergies', models.TextField()),
                ('start_year', models.CharField(max_length=255)),
                ('expected_exam_year', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BachelorProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MasterProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='iuser',
            name='bachelor_profile',
            field=models.ForeignKey(to='user_managements.BachelorProfile'),
        ),
        migrations.AddField(
            model_name='iuser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group', verbose_name='groups', blank=True, related_name='user_set'),
        ),
        migrations.AddField(
            model_name='iuser',
            name='master_profile',
            field=models.ForeignKey(to='user_managements.MasterProfile'),
        ),
        migrations.AddField(
            model_name='iuser',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission', verbose_name='user permissions', blank=True, related_name='user_set'),
        ),
    ]
