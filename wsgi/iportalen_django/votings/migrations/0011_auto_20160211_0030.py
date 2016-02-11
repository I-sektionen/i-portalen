# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0010_auto_20160210_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='body',
            field=models.TextField(verbose_name='utförlig information', null=True, blank=True, help_text='Utförligare information till frågan.'),
        ),
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(default='d', max_length=1, choices=[('d', 'Utkast'), ('o', 'Öppen'), ('c', 'Stängd')], help_text='Kan inte ändras tillbaka till draft efter att det öppnats och kan inte öppnats efter att den stängts. Det går inte heller att göra ändringar på annat än status och verifieringskod efter att draft läget lämnats.'),
        ),
    ]
