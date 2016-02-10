# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0009_auto_20160209_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.CharField(verbose_name='fråga', max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='publish_results',
            field=models.CharField(verbose_name='publicerings alternativ', max_length=1, choices=[('b', 'Gör resultaten synliga innan man röstat.'), ('a', 'Gör resultaten synliga efter att man röstat.'), ('c', 'Gör resultaten synliga när röstningen stängt.')], default='c'),
        ),
        migrations.AlterField(
            model_name='question',
            name='result',
            field=models.CharField(verbose_name='resultattyp', max_length=1, choices=[('d', 'Publik tillgång till detaljerad information om röstingen.'), ('l', 'Publik tillgång till begränsad information om röstningen.'), ('p', 'Privat åtkomst enbart för administratörer'), ('s', 'Privat åtkomst enbart för personer listade i "Användare som kan se resultatet"')], default='p'),
        ),
        migrations.AlterField(
            model_name='question',
            name='result_readers',
            field=models.ManyToManyField(verbose_name='användare som kan se resultatet', help_text='Användaren som kan se resultatet i omröstningen, används bara om resultattypen är: "Privat åtkomst enbart för personer listade i "Användare som kan se resultatet"" ', related_name='result_reader', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
