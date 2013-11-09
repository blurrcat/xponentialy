#!/usr/env/bin python
# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta


def get_intraday_url(fitbit_client, resource, base_date='today',
                     detail_level='1min', start_time='00:00',
                     end_time='23:59'):
    """
    python-fitbit API currently doesn't have intraday-activity, add one here
    :param fitbit_client: an instance of :class:`fitbit.Fitbit`
    :param resource: one of 'calories', 'steps', 'floors' or 'elevation'
    :param base_date: a string in format of 'yyyy-MM-dd' or 'today' or a
    datetime object
    :param detail_level: '1min' or '15min'
    :param start_time, end_time: a string in format of 'HH-mm' or a datetime
    object
    :return:
    """
    if resource not in ('calories', 'steps', 'floors', 'elevation'):
        raise ValueError("resource must be one of 'calories', 'steps'," +
                         " 'floors', 'elevation'")
    if not isinstance(base_date, basestring):
        base_date = base_date.strftime('%Y-%m-%d')
    if detail_level and detail_level not in ('1min', '15min'):
        raise ValueError("Detail level must be one of '1min', '15min'")
    if not isinstance(start_time, basestring):
        start_time = start_time.strftime('%H:%m')
    if not isinstance(end_time, basestring):
        end_time = end_time.strftime('%H:%m')
    parts = [fitbit_client.API_ENDPOINT, str(fitbit_client.API_VERSION),
             'user', '-', 'activities', resource, 'date', base_date, '1d',
             detail_level, 'time', start_time, end_time]

    return '/'.join(parts) + '.json'


def make_datetime(date_str, time_str):
    """
    Make a datetime object from string
    :param date_str: '%Y-%m-%d', e.g., 2013-11-10
    :param time_str: '%H:%M:%S', e.g. 23:20:02
    :return:
    """
    return dt.strptime('%s %s' % (date_str, time_str), '%Y-%m-%d %H:%M%S')


def split_datetime(dt):
    """
    Given a datetime object, return a tuple consisting a date str and a
    time str.
    :param dt: a datetime object
    :return: ('%Y-%m-%d', '%H:%M')
    """
    return dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M')


def time_range(n_days):
    """
    :param n_days:
    :return:
    """
    now = dt.utcnow()
    delta = timedelta(seconds=n_days * 86400)
    return now - delta, now


def evl(q, *fields):
    """
    Evaluate and print the result of a peewee query
    :param q: a peewee query
    :param fields: fields to print
    """
    for r in q:
        print r.id, {f: getattr(r, f) for f in fields}


def recent_days(n=30, formator=None):
    if not formator:
        formator = lambda d: d.strftime('%Y-%m-%d')
    delta = timedelta(seconds=86400)
    today = dt.utcnow()
    yield formator(today)
    for i in xrange(n - 1):
        today = today - delta
        yield formator(today)
