# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utlandsportalen', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Länder', 'verbose_name': 'Land'},
        ),
        migrations.AlterModelOptions(
            name='exchange_course',
            options={'verbose_name_plural': 'Utlandskurser', 'verbose_name': 'Utlandskurs'},
        ),
        migrations.AlterModelOptions(
            name='liu_course',
            options={'verbose_name_plural': 'Liukurser', 'verbose_name': 'Liukurs'},
        ),
        migrations.AlterModelOptions(
            name='school',
            options={'verbose_name_plural': 'Skolor', 'verbose_name': 'Skola'},
        ),
        migrations.RemoveField(
            model_name='exchange_course',
            name='is_compulsary',
        ),
        migrations.AlterField(
            model_name='exchange_course',
            name='technical_profile',
            field=models.CharField(default='NONE', verbose_name='Teknisk inriktning', choices=[('Datateknik', 'Datateknik'), ('Energiteknik', 'Energiteknik'), ('Maskinteknik', 'Maskinteknik'), ('Bioteknik', 'Bioteknik'), ('Systemteknik', 'Systemteknik'), ('Ingen', 'Ingen')], max_length=12),
        ),
    ]
