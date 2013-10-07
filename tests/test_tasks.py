#!/usr/env/bin python
# -*- coding: utf-8 -*-
import logging
import pytest
from xponentialy.tasks import task


def test_task():
    @task(1, 1, logging)
    def add_task(a, b):
        return a + b

    result = add_task(1, 2)
    assert result.get() == 3


def test_retry():

    def assert_err(msg, *args):
        print msg % args
        assert 'exception' in msg
    logging.error = assert_err

    @task(2, 1, logging)
    def add_task(a, b):
        return a + b

    result = add_task(1, '2')
    with pytest.raises(TypeError):
        result.get(timeout=3)
