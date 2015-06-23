# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0002_auto_20150623_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iuser',
            name='address',
            field=models.CharField(max_length=255, verbose_name='adress'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='allergies',
            field=models.TextField(verbose_name='allergier'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='bachelor_profile',
            field=models.ForeignKey(blank=True, to='user_managements.BachelorProfile', null=True, verbose_name='kandidatprofil'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='city',
            field=models.CharField(max_length=255, verbose_name='ort'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='expected_exam_year',
            field=models.IntegerField(choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], max_length=4, default=2020, verbose_name='förväntat examens år'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='first_name',
            field=models.CharField(max_length=50, blank=True, null=True, verbose_name='förnamn'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='gender',
            field=models.CharField(max_length=255, verbose_name='kön'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='last_name',
            field=models.CharField(max_length=50, blank=True, null=True, verbose_name='efternamn'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='master_profile',
            field=models.ForeignKey(blank=True, to='user_managements.MasterProfile', null=True, verbose_name='masterprofil'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='p_nr',
            field=models.CharField(max_length=255, verbose_name='personnummer'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='start_year',
            field=models.IntegerField(choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], max_length=4, default=2015, verbose_name='start år'),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='zip_code',
            field=models.CharField(max_length=255, verbose_name='postnummer'),
        ),
    ]
