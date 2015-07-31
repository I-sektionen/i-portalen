# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20150731_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedCostAmount',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FixedCostTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('add_tax', models.BooleanField(default=True)),
                ('tax', models.DecimalField(max_digits=5, decimal_places=2)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='VariableCostAmount',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('units', models.DecimalField(max_digits=9, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='VariableCostTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('add_tax', models.BooleanField(default=True)),
                ('tax', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.AlterField(
            model_name='custominvoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 8, 30, 18, 50, 47, 19362)),
        ),
        migrations.AlterField(
            model_name='userinvoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 8, 30, 18, 50, 47, 19362)),
        ),
        migrations.AddField(
            model_name='variablecostamount',
            name='template',
            field=models.ForeignKey(to='bookings.VariableCostTemplate'),
        ),
        migrations.AddField(
            model_name='fixedcostamount',
            name='template',
            field=models.ForeignKey(to='bookings.FixedCostTemplate'),
        ),
        migrations.AddField(
            model_name='custominvoice',
            name='fixed_costs',
            field=models.ManyToManyField(related_name='bookings_custominvoice_related', to='bookings.FixedCostAmount'),
        ),
        migrations.AddField(
            model_name='custominvoice',
            name='variable_costs',
            field=models.ManyToManyField(related_name='bookings_custominvoice_related', to='bookings.VariableCostAmount'),
        ),
        migrations.AddField(
            model_name='userinvoice',
            name='fixed_costs',
            field=models.ManyToManyField(related_name='bookings_userinvoice_related', to='bookings.FixedCostAmount'),
        ),
        migrations.AddField(
            model_name='userinvoice',
            name='variable_costs',
            field=models.ManyToManyField(related_name='bookings_userinvoice_related', to='bookings.VariableCostAmount'),
        ),
    ]
