#!/usr/env/bin python
# -*- coding: utf-8 -*-
from gevent import spawn, sleep
from gevent.event import AsyncResult


class Task(object):
    RETRY_INTERVAL = 1
    RETRY_MAX = 0
    app = None

    def __init__(self, max_retry=None, retry_interval=None):
        self.max_retry = max_retry or Task.RETRY_MAX
        self.retry_interval = retry_interval or Task.RETRY_INTERVAL

    def __call__(self, f):
        def call(*args, **kwargs):
            with self.app.app_context():
                self.app.logger.info('Start task %s(*args=%s, **kwargs=%s)',
                                     f, args, kwargs)
                return f(*args, **kwargs)

        def inner(*args, **kwargs):
            result = AsyncResult()

            def on_exception(greenlet):
                tried = greenlet.tried
                with self.app.app_context():
                    if greenlet.tried < self.max_retry:
                        self.app.logger.error(
                            'Unhandled exception in task %s(*args=%s, ' +
                            '**kwargs=%s): %s; tried %d times; retry in %ds',
                            f, args, kwargs,
                            greenlet.exception, tried, self.retry_interval
                        )
                        sleep(self.retry_interval)
                        inner(__tried=tried + 1, *args, **kwargs)
                    else:
                        self.app.logger.error(
                            'Unhandled exception in task %s(*args=%s, ' +
                            '**kwargs=%s): %s; tried %d times(max=%d); abort',
                            f, args, kwargs,
                            greenlet.exception, tried, self.max_retry
                        )
                        result.set_exception(greenlet.exception)

            def on_value(greenlet):
                with self.app.app_context():
                    self.app.logger.info(
                        'Finished task %s(*args=%s, **kwargs=%s)',
                        f, args, kwargs)
                result.set(greenlet.value)

            tried = kwargs.pop('__tried', 0)
            g_task = spawn(call, *args, **kwargs)
            g_task.tried = tried
            g_task.link_exception(on_exception)
            g_task.link_value(on_value)

            return result
        return inner


def init_app(app):
    conf = app.config
    Task.RETRY_INTERVAL = conf['TASK_RETRY_INTERVAL']
    Task.RETRY_MAX = conf['TASK_RETRY_MAX']
    Task.app = app


@Task()
def test(x):
    sleep(0)
    return x


@Task(max_retry=1, retry_interval=1)
def test_exception(x):
    raise Exception(str(x))