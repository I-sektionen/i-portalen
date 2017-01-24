# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0002_delete_iuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('in_country', models.ForeignKey(to='exchange_portal.Country')),
            ],
            options={
                'verbose_name_plural': 'Städer',
                'verbose_name': 'Stad',
            },
        ),
        migrations.RemoveField(
            model_name='school',
            name='in_country',
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='upload',
            field=models.FileField(upload_to='travel_stories/%Y%m%d/'),
        ),
        migrations.AddField(
            model_name='school',
            name='in_city',
            field=models.ForeignKey(to='exchange_portal.City', default=0),
            preserve_default=False,
        ),
    ]
