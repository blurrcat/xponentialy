#!/usr/env/bin python
# -*- coding: utf-8 -*-
from datetime import datetime

from flask import current_app
from fitbit import Fitbit
from fitbit.exceptions import HTTPException

from . import Task, StopTask
from xponentialy.models import User, Update
from xponentialy.models import get_model_by_name


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
    try:
        user = User.select(User.oauth_token, User.oauth_secret).where(
            User.id == user_id).get()
    except User.DoesNotExist:
        logger.error('User %d not found', user_id)
    else:
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
                user_id, subscriber_id, collection, method=method)
        except HTTPException as e:
            logger.error(
                'Subscription error: %s; user_id: %s, '
                'subscriber_id: %s, collection: %s', repr(e), user_id,
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


def insert_or_create(model, user_id, date, data):
    try:
        item = model.get(model.user == user_id, model.date == date)
    except model.DoesNotExist:
        item = model(user=user_id, date=date)
    item.update_from_fitbit(data)
    item.save()
    return item


def get_fitbit_client(user_id, stop_task=True):
    try:
        user = User.select(
            User.oauth_token, User.oauth_secret
        ).where(User.id == user_id).get()
    except User.DoesNotExist:
        if stop_task:
            raise StopTask('Invalid user_id: %s', user_id)
        else:
            raise
    else:
        return Fitbit(
            current_app.config['FITBIT_KEY'],
            current_app.config['FITBIT_SECRET'],
            user_key=user.oauth_token,
            user_secret=user.oauth_secret
        )


@Task()
def get_update(collection, date, user_id):
    logger = current_app.logger
    try:
        user_id = user_id.split('-')[0]
        user_id = int(user_id)
    except ValueError:
        logger.error('Invalid user_id: %s', user_id)
        return
    model = get_model_by_name(collection)
    if not model:
        logger.warning(
            'Got notifications for unregistered collection: %s',
            collection
        )
        return
    update = Update(user=user_id, type=collection)
    try:
        client = get_fitbit_client(user_id, False)
    except User.DoesNotExist:
        update.update = 'User %d not found' % user_id
    else:
        try:
            resource_access = getattr(client, collection)
            data = resource_access(date=date)
        except HTTPException as e:
            logger.error(
                'Fail to get update for %s: %s', {
                    'user': '%d' % user_id,
                    'collection': collection,
                    'date': date
                }, repr(e))
            update.update = 'Fail to get update: %s' % e
        else:
            insert_or_create(model, user_id, date, data)
            update.update = 'Update success'
    update.time_updated = datetime.utcnow()
    update.save()


def get_resource(resource_access, model, date, user_id):
    current_app.logger.info('get resource for %s, %s, %d',
                            model, date, user_id)
    try:
        data = resource_access(date=date)
    except HTTPException as e:
        current_app.logger.error(
            'Fail to get update for %s: %s', {
                'user': '%d' % user_id,
                'collection': model.__name__,
                'date': date
            }, repr(e))
    else:
        return insert_or_create(model, user_id, date, data)


@Task(max_retry=0)
def sync_history(user_id, dates, collection):
    client = get_fitbit_client(user_id)
    resource_access = getattr(client, collection)
    model = get_model_by_name(collection)

    return [get_resource(resource_access, model, date, user_id)
            for date in dates]
