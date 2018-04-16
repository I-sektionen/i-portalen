# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0010_auto_20180129_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel_story',
            name='living_text',
            field=models.TextField(verbose_name='boende', blank=True, null=True, help_text='Hur bodde du?\u2028 Hur hittade du ditt boende? Tips på eventuell mäklare eller liknande? Vilka alternativ finns?\u2028 Priser och standard?\u2028'),
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='location_text',
            field=models.TextField(verbose_name='landet och staden', blank=True, null=True, help_text='Hur upplevdes landet? Staden? Kultur? Billigt eller dyrt?'),
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='prep_text',
            field=models.TextField(verbose_name='förberedelser', blank=True, null=True, help_text='Var det några särskilda förberedelser som krävdes?\u2028 Har du några generella tips gällande ansökan? Visum?'),
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='school_text',
            field=models.TextField(verbose_name='skolan', blank=True, null=True, help_text='Geografisk placering i staden?\u2028 Hur var campus?\u2028 Var det lätt att träffa lokalbefolkning?\u2028 Hur var studentlivet? Kurser: var det lätt/svårt att få kurser? Var de lätta/svåra att få tillgodoräknade?'),
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='sparetime_text',
            field=models.TextField(verbose_name='fritid', blank=True, null=True, help_text='Vad gör man på fritiden?\u2028 Resor?\u2028 Tips på saker man inte får missa'),
        ),
        migrations.AlterField(
            model_name='travel_story',
            name='studies_text',
            field=models.TextField(verbose_name='studier', blank=True, null=True, help_text='Hur var nivån på kurserna?\u2028 Råd angående att välja kurser på plats?\u2028 Svårt att hitta kurser på engelska?\u2028 Hur var språket? (framförallt för de som läser ii eller som inte läste på engelska)'),
        ),
    ]
