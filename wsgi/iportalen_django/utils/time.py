import datetime


def now_plus_one_month():
    return datetime.datetime.now() + datetime.timedelta(days=30)


def first_day_of_week(week, year):
    ret = datetime.datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if datetime.date(year, 1, 4).isoweekday() > 4:
        ret -= datetime.timedelta(days=7)
    return ret