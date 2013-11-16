#!/usr/env/bin python
# -*- coding: utf-8 -*-
from flask import current_app
import pytest
from mock import Mock


from xponentialy import app
from xponentialy.tasks import Task, init_app
init_app(app)


def test_task():
    with app.app_context():
        @Task(1, 1)
        def add_task(a, b):
            return a + b

        result = add_task(1, 2)
        assert result.get() == 3


def test_retry():

    def assert_err(msg, *args):
        print msg % args
        assert 'exception' in msg

    with app.app_context():
        current_app.logger.error = assert_err

        @Task(0, 1)
        def add_task(a, b):
            return a + b

        result = add_task(1, '2')
        with pytest.raises(TypeError):
            result.get(timeout=2)