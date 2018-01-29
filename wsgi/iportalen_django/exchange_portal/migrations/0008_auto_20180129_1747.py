# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0007_auto_20171121_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_story',
            name='body',
        ),
        migrations.AddField(
            model_name='travel_story',
            name='living_text',
            field=models.TextField(verbose_name='boende', default=1, help_text='Hur bodde du?\u2028 Hur hittade du ditt boende? Tips på eventuell mäklare eller liknande? Vilka alternativ finns?\u2028 Priser och standard?\u2028'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='location_text',
            field=models.TextField(verbose_name='landet och staden', default=1, help_text='Hur upplevdes landet? Staden? Kultur? Billigt eller dyrt?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='other_text',
            field=models.TextField(verbose_name='övrigt', default=datetime.datetime(2018, 1, 29, 16, 47, 31, 204380, tzinfo=utc), help_text='Brödtext syns när en reseberättelse visas enskilt.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='prep_text',
            field=models.TextField(verbose_name='förberedelser', default=datetime.datetime(2018, 1, 29, 16, 47, 43, 578495, tzinfo=utc), help_text='Var det några särskilda förberedelser som krävdes?\u2028 Har du några generella tips gällande ansökan? Visum?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='school_text',
            field=models.TextField(verbose_name='skolan', default=datetime.datetime(2018, 1, 29, 16, 47, 49, 523930, tzinfo=utc), help_text='Geografisk placering i staden?\u2028 Hur var campus?\u2028 Var det lätt att träffa lokalbefolkning?\u2028 Hur var studentlivet? Kurser: var det lätt/svårt att få kurser? Var de lätta/svåra att få tillgodoräknade?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='sparetime_text',
            field=models.TextField(verbose_name='fritid', default=datetime.datetime(2018, 1, 29, 16, 47, 54, 168192, tzinfo=utc), help_text='Vad gör man på fritiden?\u2028 Resor?\u2028 Tips på saker man inte får missa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='studies_text',
            field=models.TextField(verbose_name='studier', default=datetime.datetime(2018, 1, 29, 16, 47, 58, 966304, tzinfo=utc), help_text='Hur var nivån på kurserna?\u2028 Råd angående att välja kurser på plats?\u2028 Svårt att hitta kurser på engelska?\u2028 Hur var språket? (framförallt för de som läser ii eller som inte läste på engelska)'),
            preserve_default=False,
        ),
    ]
