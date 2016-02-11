# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0006_auto_20160208_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='result',
            field=models.CharField(max_length=1, choices=[('d', 'Publik tillgång till detaljerad information om röstingen.'), ('l', 'Publik tillgång till begränsad information om röstningen.'), ('p', 'Privat åtkomst enbart för administratörer')], default='p'),
        ),
    ]
