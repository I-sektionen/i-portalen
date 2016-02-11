# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('votings', '0008_auto_20160208_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='result_readers',
            field=models.ManyToManyField(blank=True, related_name='result_reader', verbose_name='användare som kan se resultatet', help_text='Användaren som kan se resultatet i omröstningen', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='result',
            field=models.CharField(default='p', max_length=1, choices=[('d', 'Publik tillgång till detaljerad information om röstingen.'), ('l', 'Publik tillgång till begränsad information om röstningen.'), ('p', 'Privat åtkomst enbart för administratörer'), ('s', 'Privat åtkomst enbart för personer listade i result_readers')]),
        ),
    ]
