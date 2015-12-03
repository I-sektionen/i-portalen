# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organisations', '0010_auto_20151104_0128'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('post', models.CharField(verbose_name='Posten medlemmen har i organisationen', max_length=40, null=True, blank=True)),
                ('email', models.EmailField(verbose_name='Emailadress', max_length=254, null=True, blank=True, help_text='Email som är specifik för posten.')),
                ('org', models.ForeignKey(verbose_name='Medlemmens organisation', to='organisations.Organisation')),
                ('user', models.ForeignKey(verbose_name='Användare', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Organisations post',
                'verbose_name_plural': 'Organisations poster',
            },
        ),
    ]
