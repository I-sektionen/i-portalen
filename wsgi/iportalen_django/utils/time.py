from django.utils import timezone
from datetime import date as _date


def now_plus_one_month():
    return timezone.now() + timezone.timedelta(days=30)


def first_day_of_week(week, year):  # found on stackoverflow...
    ret = timezone.datetime.strptime('{year:04d}-{week:02d}-1'.format(year=year, week=week), '%Y-%W-%w')
    if _date(year, 1, 4).isoweekday() > 4:
        ret -= timezone.timedelta(days=7)
    return timezone.make_aware(ret)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timezone.timedelta(n)


def combine_date_and_time(date, time):
    return timezone.make_aware(timezone.datetime.combine(date, time))


def has_passed(time):
    if timezone.now() >= time:
        return True
    return False


def now():
    return timezone.now()


def six_months_back():
    return timezone.now()-timezone.timedelta(days=180)
