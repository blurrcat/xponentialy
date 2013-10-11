#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
from flask import current_app
from flask import request
from flask.ext.restless.views import jsonify_status_code
from flask.ext.security import current_user


def check_user():
    """
    The following pre-request operations are done here:
    * Authenticate the request;
    * Only allow queries on the current user
    * Write default user id placeholder '-' to real id

    returns None if everything is ok.
    """
    if not current_user.is_authenticated():
        current_app.logger.error('Unauthenticated request: %s from %s',
                                 request.path, request.remote_addr)
        return jsonify_status_code(
            status_code=401, message='REQUEST NOT AUTHENTICATED')
    instance_id = request.view_args.get('instid')
    if not instance_id:  # queries on collections
        current_app.logger.error(
            'Request on all users is not allowed: %s from %s',
            request.path, request.remote_addr)
        return jsonify_status_code(
            status_code=403, message='ACCESS TO ALL USERS IS DENIED')
    if instance_id == '-':
        request.view_args['instid'] = current_user.id
    elif instance_id != unicode(current_user.id):
        current_app.logger.error(
            'Requested user is not the current user: %s from %s',
            request.path, request.remote_addr)
        return jsonify_status_code(
            status_code=403, message='ACCESS TO OTHER USERS IS DENIED')


def create_views(app, api_manager):
    """
    Create API endpoints using a bounded instance of
    :class:`flask.ext.restless.APIManager`.
    """
    from xponentialy import models
    config = app.config
    url_prefix = '/api/%s' % config['API_VERSION']
    # User
    user_api = api_manager.create_api_blueprint(
        models.User,
        url_prefix=url_prefix,
        methods=['GET', 'PUT'],
    )
    user_api.before_request(check_user)
    app.register_blueprint(user_api)

    # Badge
    api_manager.create_api(
        models.Badge,
        url_prefix=url_prefix,
        methods=['GET'],
    )

    # Challenge
    api_manager.create_api(
        models.Challenge,
        url_prefix=url_prefix,
        methods=['GET'],
    )



