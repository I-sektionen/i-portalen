import datetime


def now_plus_one_month():
    return datetime.datetime.now() + datetime.timedelta(days=30)
