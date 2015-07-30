# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('bookable', models.ForeignKey(to='bookings.Bookable')),
            ],
        ),
        migrations.CreateModel(
            name='BookingSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('bookable', models.ForeignKey(to='bookings.Bookable')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='slot',
            field=models.ForeignKey(to='bookings.BookingSlot'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Bokad av'),
        ),
    ]
