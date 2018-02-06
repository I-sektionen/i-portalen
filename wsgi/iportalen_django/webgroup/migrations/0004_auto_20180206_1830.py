# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgroup', '0003_groupings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='course',
        ),
        migrations.RemoveField(
            model_name='examresult',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='groupings',
            name='courses',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.DeleteModel(
            name='ExamResult',
        ),
        migrations.DeleteModel(
            name='Groupings',
        ),
    ]
