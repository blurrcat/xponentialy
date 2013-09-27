#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
import os
from flask import Flask


def create_app(config_file):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    try:
        app.config.from_envvar('FLASK_EB_CONFIG')  # try load production config
    except RuntimeError:
        pass

    from xponentialy.views import admin
    from xponentialy.views import api
    from xponentialy.models import db

    admin.init_app(app)
    api.init_app(app)
    db.init_app(app)

    return app
