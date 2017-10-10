#!/usr/bin/env python3

"""Various utils for dealing with the API"""

import pytz
import datetime
import pytimeparse


def parse_date(date, fallback=None):
    if isinstance(date, datetime.date):
        return date
    rv = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return rv


def parse_timedelta(timedelta):
    duration = pytimeparse.parse(timedelta)
    return datetime.timedelta(seconds=duration)


def parse_time(time):
    ts = pytimeparse.parse(time)
    return datetime.datetime.fromtimestamp(ts, pytz.UTC).time()


def difftime(t1, t2):
    "Naive diff between two datetime.time objects. Ignores TZ"

    dt1 = datetime.datetime(2000, 1, 15, t1.hour, t1.minute, t1.second, tzinfo=t1.tzinfo)
    dt2 = datetime.datetime(2000, 1, 15, t2.hour, t2.minute, t2.second, tzinfo=t2.tzinfo)

    return dt1 - dt2
