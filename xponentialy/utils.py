#!/usr/env/bin python
# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta


def intraday_time_series(fitbit_client, resource, base_date='today',
                         detail_level='15min', start_time='00:00'):
    """
    python-fitbit API currently doesn't have intraday-activity, add one here
    :param fitbit_client: an instance of :class:`fitbit.Fitbit`
    :param resource: one of 'calories', 'steps', 'floors' or 'elevation'
    :param base_date: a string in format of 'yyyy-MM-dd' or 'today' or a
        datetime object
    :param detail_level: '1min' or '15min'
    :param start_time: a string in format of 'HH-mm' or a datetime object
    :return:
    """
    if resource not in ('calories', 'steps', 'floors', 'elevation'):
        raise ValueError("resource must be one of 'calories', 'steps', 'floors', 'elevation'")
    if not isinstance(base_date, basestring):
        base_date = base_date.strftime('%Y-%m-%d')
    if detail_level and detail_level not in ('1min', '15min'):
        raise ValueError("Detail level must be one of '1min', '15min'")
    if not isinstance(start_time, basestring):
        start_time = start_time.strftime('%H:%m')
    parts = [fitbit_client.API_ENDPOINT, str(fitbit_client.API_VERSION),
             'user', '-', 'activities', resource, 'date', base_date,
             detail_level, 'time', start_time]

    url = '/'.join(parts) + '.json'

    return fitbit_client.make_request(url)


def time_range(n_days):
    """
    :param n_days:
    :return:
    """
    now = dt.utcnow()
    delta = timedelta(seconds=n_days * 86400)
    return now - delta, now