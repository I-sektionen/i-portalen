# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_portal', '0014_auto_20180208_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_story',
            name='time_abroad',
        ),
        migrations.AddField(
            model_name='travel_story',
            name='term_abroad',
            field=models.CharField(verbose_name='termin utomlands', max_length=5, default='HT', choices=[('HT', 'HT'), ('VT', 'VT'), ('Helår', 'Helår')], help_text='Termin du var utomlands'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travel_story',
            name='year_abroad',
            field=models.IntegerField(verbose_name='tid utomlands', default=2014, choices=[(1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)], help_text='År när du var utomlands'),
            preserve_default=False,
        ),
    ]
