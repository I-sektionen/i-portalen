# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_managements', '0004_auto_20150623_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iuser',
            name='expected_exam_year',
            field=models.IntegerField(verbose_name='förväntat examens år', choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2020),
        ),
        migrations.AlterField(
            model_name='iuser',
            name='start_year',
            field=models.IntegerField(verbose_name='start år', choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2015),
        ),
    ]
