# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0002_bookable_max_number_of_bookings'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomInvoice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('due', models.DateField(default=datetime.datetime(2015, 8, 30, 13, 17, 0, 73128))),
                ('recipient', models.CharField(max_length=400)),
                ('email', models.CharField(max_length=800)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserInvoice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('due', models.DateField(default=datetime.datetime(2015, 8, 30, 13, 17, 0, 73128))),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='booking',
            options={'permissions': (('unlimited_num_of_bookings', 'Unlimited number of bookings'),)},
        ),
        migrations.AlterField(
            model_name='bookable',
            name='max_number_of_bookings',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set([('slot', 'bookable', 'date')]),
        ),
        migrations.AddField(
            model_name='userinvoice',
            name='booking',
            field=models.OneToOneField(to='bookings.Booking'),
        ),
        migrations.AddField(
            model_name='userinvoice',
            name='recipient',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='custominvoice',
            name='booking',
            field=models.OneToOneField(to='bookings.Booking'),
        ),
    ]
