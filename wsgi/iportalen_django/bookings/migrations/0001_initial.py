# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookable',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=512)),
                ('max_number_of_bookings', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('bookable', models.ForeignKey(to='bookings.Bookable')),
                ('user', models.ForeignKey(verbose_name='Bokad av', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('unlimited_num_of_bookings', 'Unlimited number of bookings'),),
            },
        ),
        migrations.CreateModel(
            name='BookingSlot',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('bookable', models.ForeignKey(to='bookings.Bookable')),
            ],
        ),
        migrations.CreateModel(
            name='FixedCostAmount',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='FixedCostTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=400)),
                ('add_tax', models.BooleanField(default=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=5)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('due', models.DateField(default=datetime.datetime(2015, 9, 24, 7, 25, 21, 689961))),
                ('booking', models.ForeignKey(to='bookings.Booking')),
            ],
        ),
        migrations.CreateModel(
            name='PartialBooking',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateField()),
                ('booking', models.ForeignKey(related_name='Bookings', to='bookings.Booking')),
                ('slot', models.ForeignKey(to='bookings.BookingSlot')),
            ],
        ),
        migrations.CreateModel(
            name='VariableCostAmount',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('units', models.DecimalField(max_digits=9, decimal_places=2)),
                ('invoice', models.ForeignKey(to='bookings.Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='VariableCostTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=400)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('add_tax', models.BooleanField(default=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=5)),
                ('unit_name', models.CharField(max_length=30, default='st')),
            ],
        ),
        migrations.AddField(
            model_name='variablecostamount',
            name='template',
            field=models.ForeignKey(to='bookings.VariableCostTemplate'),
        ),
        migrations.AddField(
            model_name='fixedcostamount',
            name='invoice',
            field=models.ForeignKey(to='bookings.Invoice'),
        ),
        migrations.AddField(
            model_name='fixedcostamount',
            name='template',
            field=models.ForeignKey(to='bookings.FixedCostTemplate'),
        ),
        migrations.AlterUniqueTogether(
            name='partialbooking',
            unique_together=set([('slot', 'date')]),
        ),
    ]
