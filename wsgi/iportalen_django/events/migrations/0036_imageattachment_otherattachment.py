# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import events.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0035_event_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAttachment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('img', models.ImageField(verbose_name='eventlbild', upload_to=events.models._image_file_path)),
                ('thumbnail', models.ImageField(blank=True, null=True, verbose_name='förhandsvisning', upload_to=events.models._image_file_path)),
                ('caption', models.CharField(max_length=100)),
                ('event', models.ForeignKey(to='events.Event')),
                ('modified_by', models.ForeignKey(related_name='event_image_uploader', null=True, verbose_name='användare', help_text='Uppladdat av.', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
        ),
        migrations.CreateModel(
            name='OtherAttachment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('file', models.FileField(verbose_name='eventlbilaga', upload_to=events.models._file_path)),
                ('display_name', models.CharField(max_length=160)),
                ('file_name', models.CharField(blank=True, max_length=300)),
                ('event', models.ForeignKey(to='events.Event')),
                ('modified_by', models.ForeignKey(related_name='event_attachment_uploader', null=True, verbose_name='användare', help_text='Uppladdat av.', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL)),
            ],
        ),
    ]
