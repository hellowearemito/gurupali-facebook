from datetime import timedelta


def add_month(t, n=1):
    one_day = timedelta(days=1)
    for i in range(0, n):
        one_month_later = t + one_day
        while one_month_later.month == t.month:
            one_month_later += one_day
        t = one_month_later
    return one_month_later


def profile_str(value, name="Name"):
    return {
        "name": name,
        "type": "str",
        "value": value
    }


def profile_stat(stats, _id, name):
    return {
        "name": name,
        "type": "line",
        "values": [[stat[0].strftime('%Y-%m'), stat[1].get(_id, 0)]
                   for stat in stats]
    }
