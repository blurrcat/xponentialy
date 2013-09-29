#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
from flask import Flask
from flask.ext.restless import APIManager
from flask.ext.admin import Admin


def create_database(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)
    try:
        app.config.from_envvar('FLASK_EB_CONFIG')  # try load production config
    except RuntimeError:
        pass
    from models import db
    db.init_app(app)
    # import models
    db.create_all(app=app)


def create_app(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)
    try:
        app.config.from_envvar('FLASK_EB_CONFIG')  # try load production config
    except RuntimeError:
        pass
    from models import db
    db.init_app(app)

    from xponentialy import views
    api = APIManager(app)
    views.api.create_views(api)

    admin = Admin(app)
    views.admin.create_views(admin, db)

    return app


if __name__ == '__main__':
    create_database('config')