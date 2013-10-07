#!/usr/env/bin python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from datetime import datetime
from gevent import spawn, sleep
from gevent.event import AsyncResult
from flask import current_app
from fitbit import Fitbit
from fitbit.exceptions import HTTPException

from xponentialy.models import User, Update, db
from xponentialy.models.fitbit import get_model_by_name


class Task(object):
    RETRY_INTERVAL = 1
    RETRY_MAX = 0
    app = None

    def __init__(self, max_retry=None, retry_interval=None, logger=None):
        self.max_retry = max_retry or Task.RETRY_MAX
        self.retry_interval = retry_interval or Task.RETRY_INTERVAL
        self.logger = logger
        self.result = AsyncResult()
        self.tried = 0

    def __call__(self, f):

        def call(*args, **kwargs):
            if self.logger:
                self.logger.info('Start task %s(%s, %s)', f, *args, **kwargs)
            with Task.app.app_context():
                return f(*args, **kwargs)

        def inner(*args, **kwargs):
            def on_exception(greenlet):
                if self.tried < self.max_retry:
                    if self.logger:
                        self.logger.error(
                            'Unhandled exception in task: %s(%s, %s): %s; ' +
                            'tried %d times; retry in %d sec', f, args, kwargs,
                            greenlet.exception, self.tried, self.retry_interval
                        )
                    self.tried += 1
                    sleep(self.retry_interval)
                    inner(*args, **kwargs)
                else:
                    if self.logger:
                        self.logger.error(
                            'Unhandled exception in task: %s(%s, %s): %s; ' +
                            'tried %d times; abort', f, args, kwargs,
                            greenlet.exception, self.tried
                        )
                    self.result.set_exception(greenlet.exception)

            def on_value(greenlet):
                if self.logger:
                    self.logger.info('Finished task %s(%s, %s)',
                                      f, *args, **kwargs)
                self.result.set(greenlet.value)

            g_task = spawn(call, *args, **kwargs)
            g_task.link_exception(on_exception)
            g_task.link_value(on_value)

            return self.result
        return inner


def init_app(app):
    conf = app.config
    Task.RETRY_INTERVAL = conf['TASK_RETRY_INTERVAL']
    Task.RETRY_MAX = conf['TASK_RETRY_MAX']
    Task.app = app


@Task()
def subscribe(user_id, subscriber_id, delete=False, collection=None):
    """
    Subscribe/unsubscribe a user for his fitbit data
    :param user_id: user's XP account id
    :param subscriber_id: subscriber endpoint id
    :param delete: set to True to unsubscribe
    :param collection: one of sleep, foods, body, activities.
        Default to all of them.
    :return: None
    """
    logger = current_app.logger
    user = User.query.with_entities(
        User.oauth_token, User.oauth_secret).filter_by(id=user_id).first()
    if user:
        client = Fitbit(
            current_app.config['FITBIT_KEY'],
            current_app.config['FITBIT_SECRET'],
            user_key=user.oauth_token,
            user_secret=user.oauth_secret
        )
        if delete:
            method = 'DELETE'
        else:
            method = 'POST'
        try:
            resp = client.subscription(
                subscriber_id, user_id, collection, method=method)
        except HTTPException as e:
            logger.error(
                'Subscription error: %s; user_id: %s, '
                'subscription_id: %s, collection: %s', e, user_id,
                subscriber_id, collection)
        else:
            # resp:
            # {
            #   u'ownerId': u'27LBMG', u'collectionType': u'user',
            #   u'ownerType': u'user', u'subscriberId': u'ec2-dev',
            #   u'subscriptionId': u'ec2-dev'
            # }
            logger.info('Subscription success: %s', resp)
            return resp
    else:
        logger.error('User %d not found', user_id)


@Task()
def get_update(collection, date, user_id):
    logger = current_app.logger
    model = get_model_by_name(collection)
    if not model:
        logger.warning(
            'Got notifications for unregistered collection: %s',
            collection
        )
        return
    user = User.query.with_entities(
        User.oauth_token, User.oauth_secret).filter_by(id=user_id).first()
    update = Update(user_id=user_id, type=collection)
    if user:
        client = Fitbit(
            current_app.config['FITBIT_KEY'],
            current_app.config['FITBIT_SECRET'],
            user_key=user.oauth_token,
            user_secret=user.oauth_secret
        )
        try:
            resource_access = getattr(client, collection)
            data = resource_access(date=date)
        except HTTPException as e:
            logger.error(
                'Fail to get update for %s: %s', {
                    'user': '%d' % user_id,
                    'collection': collection,
                    'date': date
                }, e)
            update.update = 'Fail to get update: %s' % e
            update.time_updated = datetime.now()
        else:
            item = model(user_id=user_id, date=date)
            item.update(data)
            db.session.merge(item)
            update.update = 'update success'
            update.time_updated = datetime.now()
    else:
        update.update = 'User %d not found' % user_id
        update.time_updated = datetime.now()
    # will never reach here if any unhandled exception happened,
    # like request timeout. In that case, the 'update_time' field
    # will be empty. We may setup a cronjob to check them later
    db.session.merge(update)
    db.session.commit()
