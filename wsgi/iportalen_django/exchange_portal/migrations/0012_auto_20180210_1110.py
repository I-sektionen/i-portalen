# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0011_auto_20180129_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Världsdel',
                'verbose_name_plural': 'Världsdelar',
            },
        ),
        migrations.AlterField(
            model_name='exchange_course',
            name='technical_profile',
            field=models.CharField(verbose_name='Teknisk inriktning', max_length=12, default='NONE', choices=[('D', 'D'), ('E', 'E'), ('M', 'M'), ('B', 'B'), ('S', 'S'), ('Övr', 'Övr')]),
        ),
        migrations.AddField(
            model_name='country',
            name='in_continent',
            field=models.ForeignKey(null=True, to='exchange_portal.Continent'),
        ),
    ]
