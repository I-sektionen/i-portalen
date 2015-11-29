# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('bookings', '0002_auto_20150825_0735'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookable',
            options={'verbose_name': 'bokningsbart objekt', 'verbose_name_plural': 'bokningsbara objekt'},
        ),
        migrations.AlterModelOptions(
            name='booking',
            options={'verbose_name': 'bokning',
                     'permissions': (('unlimited_num_of_bookings', 'Unlimited number of bookings'),),
                     'verbose_name_plural': 'bokningar'},
        ),
        migrations.AlterModelOptions(
            name='bookingslot',
            options={'verbose_name': 'bokningsblock', 'verbose_name_plural': 'bokningsblock'},
        ),
        migrations.AlterModelOptions(
            name='fixedcosttemplate',
            options={'verbose_name': 'mall', 'verbose_name_plural': 'mallar för fasta kostnader'},
        ),
        migrations.AlterModelOptions(
            name='invoice',
            options={'verbose_name': 'faktura', 'verbose_name_plural': 'fakturor'},
        ),
        migrations.AlterModelOptions(
            name='partialbooking',
            options={'verbose_name': 'delbokning', 'verbose_name_plural': 'delbokninar'},
        ),
        migrations.AlterModelOptions(
            name='variablecosttemplate',
            options={'verbose_name': 'mall', 'verbose_name_plural': 'mallar för rörliga kostnader'},
        ),
        migrations.AlterField(
            model_name='booking',
            name='bookable',
            field=models.ForeignKey(verbose_name='boknings objekt', to='bookings.Bookable'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(verbose_name='bokad av', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fixedcosttemplate',
            name='add_tax',
            field=models.BooleanField(default=True, verbose_name='Lägg till moms?'),
        ),
        migrations.AlterField(
            model_name='fixedcosttemplate',
            name='amount',
            field=models.DecimalField(verbose_name='belopp', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='fixedcosttemplate',
            name='tax',
            field=models.DecimalField(verbose_name='moms', null=True, max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='fixedcosttemplate',
            name='title',
            field=models.CharField(verbose_name='namn', max_length=400),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='booking',
            field=models.ForeignKey(verbose_name='bokning', to='bookings.Booking'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DateField(default=datetime.datetime(2015, 12, 11, 21, 12, 22, 867297),
                                   verbose_name='förfallo dag'),
        ),
        migrations.AlterField(
            model_name='partialbooking',
            name='booking',
            field=models.ForeignKey(to='bookings.Booking', related_name='bookings'),
        ),
    ]
