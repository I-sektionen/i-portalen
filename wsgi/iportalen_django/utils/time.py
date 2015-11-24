from django.utils import timezone
from datetime import date


def now_plus_one_month():
    return timezone.datetime.now() + timezone.timedelta(days=30)


def first_day_of_week(week, year):
    ret = timezone.datetime.strptime('{year:04d}-{week:02d}-1'.format(year=year, week=week), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        ret -= timezone.timedelta(days=7)
    return ret
