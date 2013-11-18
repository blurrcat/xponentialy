#!/usr/env/bin python
# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, timedelta

from flask import current_app
from fitbit import Fitbit
from fitbit.exceptions import HTTPException, HTTPUnauthorized

from xponentialy.tasks import Task
from xponentialy import db
from xponentialy.models import User, Update, IntradayActivity
from xponentialy.models import get_model_by_name
from xponentialy.utils import get_intraday_url
from xponentialy.utils import make_datetime


def _handle_unauthorised(user, exception):
    if isinstance(exception, HTTPUnauthorized):
        # invalid token-secret pair, reset to empty
        # TODO: ask user to reconnect the next time he logs in
        user.oauth_token = ''
        user.oauth_secret = ''
        user.save()


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
            _handle_unauthorised(user, e)
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
    """
    Insert or create an entry of Activity or sleep
    :param model: :class:`xponentialy.models.Sleep` or
        :class:`xponentialy.models.Activity`
    :param user_id: owner id
    :param date: date of the entry
    :param data: resource data returned by fitbit
    :return: the new or updated instance
    """
    item = model.get_or_create(user=user_id, date=date)
    item.update_from_fitbit(data)
    item.save()
    return item


@Task()
def get_update(collection, date, user_id):
    logger = current_app.logger
    now = datetime.utcnow()  # TODO: should be user's local time
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
        user = User.get(User.id == user_id)
    except User.DoesNotExist:
        update.update = 'User %d not found' % user_id
    else:
        client = user.get_fitbit_client()
        try:
            resource_access = getattr(client, collection)
            data = resource_access(date=date)
            print data
        except HTTPException as e:
            _handle_unauthorised(user, e)
            logger.error(
                'Fail to get update for %s: %s', {
                    'user': '%d' % user_id,
                    'collection': collection,
                    'date': date
                }, repr(e))
            update.update = 'Fail to get update: %s' % repr(e)
        else:
            item = insert_or_create(model, user_id, date, data)
            update.update = 'Update success'
            conf = current_app.config
            if collection == 'activities' and conf['FITBIT_INTRADAY_ENABLED']:
                # only update changed resources
                resources = [r for r in conf['FITBIT_INTRADAY_RESOURCES']
                             if getattr(item, r)]
                get_intraday(
                    user, client, date, '00:00',
                    detail_level=conf['FITBIT_INTRADAY_DETAIL_LEVEL'],
                    resources=resources
                )
    update.time_updated = now
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


def get_intraday(user, client, base_date, start_time, detail_level, resources):
    """
    Get intraday data from base_date:start_time to now.
    """
    if not resources:
        return
    date = datetime.strptime(base_date, '%Y-%m-%d')
    logger = current_app.logger
    existing = IntradayActivity.select().where(
        IntradayActivity.user == user,
        IntradayActivity.activity_time.between(
            date, date + timedelta(days=1)))
    cache = defaultdict(lambda: IntradayActivity(user=user))
    dirty = set()
    for item in existing:
        cache[item.activity_time.strftime('%H:%M:%S')] = item
    for resource in resources:
        url = get_intraday_url(client, resource,
                               detail_level=detail_level,
                               base_date=base_date,
                               start_time=start_time)
        try:
            resp = client.make_request(url)
        except HTTPException as e:
            _handle_unauthorised(user, e)
            logger.error("Can't get intraday %s for user %s: %s",
                         resource, user.id, repr(e))
            continue
        else:
            date_str = resp.get('activities-%s' % resource)[0]['dateTime']
            dataset = resp.get(
                'activities-%s-intraday' % resource)['dataset']
            precision = current_app.config['FITBIT_FLOAT_PRECISION']
            for item in dataset[:-1]:
                if item['value']:  # only store non-empty values
                    intraday_activity = cache[item['time']]
                    item['value'] = round(item['value'], precision)
                    intraday_activity.activity_time = make_datetime(
                        date_str, item['time'])
                    if intraday_activity.update_from_fitbit(item, resource):
                        dirty.add(intraday_activity)
    with db.database.transaction():
        logger.info('%d intraday activity records updated', len(dirty))
        for item in dirty:
            item.save()


@Task(max_retry=0)
def sync_history(user_id, dates, collection):
    user = User.get(User.id == user_id)
    client = user.get_fitbit_client()
    resource_access = getattr(client, collection)
    model = get_model_by_name(collection)

    return [get_resource(resource_access, model, date, user_id)
            for date in dates]


@Task()
def get_user_profile(user):
    client = user.get_fitbit_client()
    profile = client.user_profile_get()['user']
    user.fitbit = profile.get('encodedId')
    user.avatar = profile.get('avatar')
    user.gender = profile.get('gender')
    if not (user.first_name or user.last_name):
        # only use names from fitbit if they are not set already
        fullname = profile.get('fullName')
        if fullname:
            parts = fullname.split(' ', 1)
            if len(parts) == 2:
                user.first_name, user.last_name = parts
    user.utc_offset = profile.get('offsetFromUTCMillis', 0) / 1000
    user.save()

if __name__ == '__main__':
    from xponentialy import load_app, app
    load_app()
    with app.app_context():
        get_update('activities', '2013-10-07', '2')