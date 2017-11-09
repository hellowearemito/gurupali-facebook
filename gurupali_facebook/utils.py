from datetime import timedelta


def add_month(t, n=1):
    one_day = timedelta(days=1)
    for i in range(0, n):
        one_month_later = t + one_day
        while one_month_later.month == t.month:
            one_month_later += one_day
        t = one_month_later
    return one_month_later
