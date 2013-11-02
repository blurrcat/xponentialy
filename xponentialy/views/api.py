#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>
import datetime

from flask import g, jsonify, request, abort
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


class RestrictOwnerIDResource(RestrictOwnerResource):
    # RestrictOwnerResource compares user objects to do validation
    # However g.user == resource.user maybe False since only auth related
    # fields are loaded into g.user.
    # It makes more sense to compare pk here.

    def validate_owner(self, user, obj):
        return user.id == getattr(obj, self.owner_field).id


class StrictOwnerResource(RestrictOwnerIDResource):
    """
    For GET requests, only return objects owned by the current user
    """
    def get_query(self):
        return self.model.select().where(self.model.user == g.user.id)


class XpRestAPI(RestAPI):

    def response_auth_failed(self):
        # do not pop up user/password dialog
        abort(401)


class SessionAuthentication(Authentication):

    def authorize(self):
        # todo: CSRF protection
        return auth.get_logged_in_user() is not None


class LeaderBoardMixin(object):

    def is_leaderboard(self):
        return 'leaders' in request.args

    def get_leaderboard_time_range(self):
        try:
            days = int(request.args.get('time_range', 7))
        except ValueError:
            abort(400)
        else:
            if days < 0:
                abort(400)
            return days

    def get_leaderboard_meta(self, meta):
        if self.is_leaderboard():
            meta.update({
                'leaders': True,
                'time_range': self.get_leaderboard_time_range()
            })
        return meta


class UserResource(RestResource, LeaderBoardMixin):
    fields = ['id', 'username', 'avatar', 'gender', 'points', 'company']
    include_resources = []

    def get_query(self):
        if self.is_leaderboard():
            days = self.get_leaderboard_time_range()
            cid = auth.get_current_company_id()
            return self.model.get_leaders(cid, days)
        else:
            return self.model.select().where(
                self.model.company == auth.get_current_company_id())

    def prepare_data(self, obj, data):
        data['challenge_num'] = obj.challenge_num
        data['rank'] = obj.rank
        if self.is_leaderboard():
            data['challenge_completed'] = obj.challenge_completed
        return data

    def get_request_metadata(self, paginated_query):
        meta = super(UserResource, self).get_request_metadata(paginated_query)
        self.get_leaderboard_meta(meta)
        return meta


class BadgeResource(RestResource):
    fields = ['id', 'name', 'description', 'avatar']

    def prepare_data(self, obj, data):
        data['friendly_time'] = '2 days ago'  # todo: implement friendly time
        return data


class UserBadgeResource(RestrictOwnerIDResource):
    exclude = ('id',)
    include_resources = {
        'badge': BadgeResource,
    }


class ChallengeResource(RestrictOwnerIDResource):

    def get_serializer(self):
        return api_serializer


class ChallengeParticipantResource(StrictOwnerResource):

    def deserialize_object(self, data, instance):
        user = models.User.select(models.User.house).where(
            models.User.id == auth.get_current_user_id()
        ).get()
        data['house'] = user.house.id
        return super(
            ChallengeParticipantResource, self
        ).deserialize_object(data, instance)


class ActivityResource(StrictOwnerResource):
    pass


class IntradayActivityResource(StrictOwnerResource):
    pass


class HouseResource(RestResource, LeaderBoardMixin):

    def get_query(self):
        if self.is_leaderboard():
            days = self.get_leaderboard_time_range()
            cid = auth.get_current_company_id()
            return self.model.get_leaders(cid, days)
        else:
            return self.model.select().where(
                self.model.company == auth.get_current_company_id())

    def prepare_data(self, obj, data):
        # data['rank'] = obj.rank  # todo: implement house rank
        if self.is_leaderboard():
            data['points'] = obj.points  # todo: implement house points
        else:
            data['members'] = [
                serializer.serialize_object(
                    u, {models.User: UserResource.fields})
                for u in obj.users]
        return data

    def get_request_metadata(self, paginated_query):
        meta = super(HouseResource, self).get_request_metadata(paginated_query)
        self.get_leaderboard_meta(meta)
        return meta


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

