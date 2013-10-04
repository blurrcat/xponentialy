#!/usr/env/bin python
# -*- coding: utf-8 -*-
from celery import Celery
from flask import current_app
from fitbit import Fitbit
from fitbit.exceptions import HTTPException

from xponentialy import config_app
from xponentialy.models import User
from xponentialy.models.fitbit import get_model_by_name

app, db = config_app()
celery = Celery(app.import_name,
                broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
TaskBase = celery.Task


class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)
celery.Task = ContextTask


@celery.task()
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
        except Exception as e:
            raise subscribe.retry(exc=e)
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


@celery.task
def get_update(collection, date, user_id):
    logger = current_app.logger
    model = get_model_by_name(collection)
    if not model:
        logger.warning(
            'Got notifications for unregistered collection: %s',
            collection
        )
    user = User.query.get(user_id)
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
                    'user': '%s' % user.username,
                    'collection': collection,
                    'date': date
                }, e)
        except Exception as e:
            raise get_update.retry(exc=e)
        else:
            item = model.query.get((user.id, date))
            if not item:
                item = model(user=user, date=date)
            item.update(data)
            db.session.commit()
            return data, item
    else:
        logger.error('User %d not found', user_id)


@celery.task
def celery_test_task(a, b):
    current_app.logger.info('Execute celery test task: %d + %d', a, b)
    return a + b