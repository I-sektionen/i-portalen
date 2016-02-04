# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import articles.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0028_auto_20160104_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAttachment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(verbose_name='artikelbild', upload_to=articles.models._image_file_path)),
                ('thumbnail', models.ImageField(blank=True, verbose_name='förhandsvisning', upload_to=articles.models._image_file_path, null=True)),
                ('caption', models.CharField(max_length=100)),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
        ),
        migrations.CreateModel(
            name='OtherAttachment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(verbose_name='artikelbilaga', upload_to=articles.models._file_path)),
                ('display_name', models.CharField(max_length=160)),
                ('file_name', models.CharField(blank=True, max_length=300)),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
        ),
    ]
