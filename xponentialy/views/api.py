#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>
import datetime

from flask import g, Response, jsonify
from flask.ext.peewee.rest import RestResource
from flask.ext.peewee.rest import RestrictOwnerResource
from flask.ext.peewee.rest import Authentication
from flask.ext.peewee.rest import RestAPI
from flask.ext.peewee.serializer import Serializer

from xponentialy import app
from xponentialy import models
from xponentialy.auth import auth


class APISerializer(Serializer):
    """
    Patch the standard serializer so it can serialize `datetime.timedelta`
    objects.
    """
    def convert_value(self, value):
        if isinstance(value, datetime.timedelta):
            return value.total_seconds()
        return super(APISerializer, self).convert_value(value)


class StrictOwnerResource(RestrictOwnerResource):
    """
    For GET requests, only return objects owned by the current user
    """
    def get_query(self):
        return self.model.select().where(self.model.user == g.user.id)


class XpRestAPI(RestAPI):

    def response_auth_failed(self):
        # do not pop up user/password dialog
        return Response('Authentication failed', 401)


class SessionAuthentication(Authentication):

    def authorize(self):
        # todo: CSRF protection
        return auth.get_logged_in_user() is not None


class UserResource(RestResource):
    fields = ['id', 'username', 'avatar', 'gender', 'points', 'company']
    include_resources = []

    def get_query(self):
        User = self.model
        return User.select().where(
            User.company == auth.get_current_company_id())

    def prepare_data(self, obj, data):
        data['challenge_num'] = obj.challenge_num
        data['rank'] = obj.rank
        return data


class BadgeResource(RestResource):
    fields = ['id', 'name', 'description', 'avatar']

    def prepare_data(self, obj, data):
        data['friendly_time'] = '2 days ago'  # todo: implement friendly time
        return data


class UserBadgeResource(RestrictOwnerResource):
    exclude = ('id',)
    include_resources = {
        'badge': BadgeResource,
    }


class ChallengeResource(RestrictOwnerResource):

    def get_serializer(self):
        return api_serializer


class ChallengeParticipantResource(StrictOwnerResource):
    pass


class ActivityResource(StrictOwnerResource):
    pass


class IntradayActivityResource(StrictOwnerResource):
    pass


class HouseResource(RestResource):

    def get_query(self):
        return self.model.select().where(
            self.model.company == auth.get_current_company_id())

    def prepare_data(self, obj, data):
        data['rank'] = 1  # todo: implement house rank
        data['points'] = 1000  # todo: implement house points
        data['members'] = [
            serializer.serialize_object(u, {models.User: UserResource.fields})
            for u in obj.users]
        return data


serializer = Serializer()
api_serializer = APISerializer()
api = XpRestAPI(app, prefix='/api/%s' % app.config['API_VERSION'],
                default_auth=SessionAuthentication(
                    protected_methods=['GET', 'PUT', 'POST', 'DELETE']))

api.register(models.User, UserResource, allowed_methods=['GET', 'PUT'])
api.register(models.Badge, BadgeResource, allowed_methods=['GET'])
api.register(models.UserBadge, UserBadgeResource, allowed_methods=['GET'])
api.register(models.Challenge, ChallengeResource, allowed_methods=['GET'])
api.register(models.ChallengeParticipant, ChallengeParticipantResource,
             allowed_methods=['GET', 'PUT', 'POST', 'DELETE'])
api.register(models.Activity, ActivityResource, allowed_methods=['GET'])
api.register(models.IntradayActivity, IntradayActivityResource,
             allowed_methods=['GET'])
api.register(models.House, HouseResource, allowed_methods=['GET'])


@api.blueprint.route('/')
def api_index():
    endpoints = []
    for rule in app.url_map.iter_rules():
        r = rule.rule
        if r.startswith('/api'):
            endpoints.append({
                'endpoint': r,
                'methods': list(rule.methods)
            })
    return jsonify({
        '!description': 'test only',
        'endpoints': endpoints
    })

api.setup()

