#!/usr/env/bin python
# -*- coding: utf-8 -*-
from xponentialy.utils import make_datetime, split_datetime
from datetime import datetime


def test_make_datetime():
    dt = make_datetime('2013-10-11', '23:10:00')
    assert dt.year == 2013
    assert dt.hour == 23


def test_split_datetime():
    dt = datetime(2013, 10, 11, 23, 10)
    d, t = split_datetime(dt)
    assert d == '2013-10-11'
    assert t == '23:10'
