#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 Harry <blurrcat@gmail.com>

"""

"""
__version__ = '0.2.0a1'
from gevent import monkey
monkey.patch_all()

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.peewee.db import Database

app = Flask(__name__)
app.config.from_object('config')
try:
    # try load deployment config
    app.config.from_envvar('DEPLOYMENT_CONFIG')
except RuntimeError:
    import os
    app.logger.warning(
        'Cannot load DEPLOYMENT_CONFIG, ignore; os.environ: %s',
        os.environ)
app.config['FITBIT_OAUTH']['consumer_key'] = app.config['FITBIT_KEY']
app.config['FITBIT_OAUTH']['consumer_secret'] = app.config['FITBIT_SECRET']

db = Database(app)
db.connect_db()


def load_app():
    conf = app.config
    # logging
    handler = RotatingFileHandler(
        conf['LOG_FILE'], maxBytes=conf['LOG_MAX_BYTES'],
        backupCount=conf['LOG_BACKUP_COUNT'])
    if conf['DEBUG']:
        level = logging.DEBUG
    else:
        level = conf['LOG_LEVEL']
    handler.setLevel(level)
    formatter = logging.Formatter(conf['LOG_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # views
    import views
    app.register_blueprint(views.xp_bp)
    app.register_blueprint(views.fitbit_bp, url_prefix='/fitbit')

    # tasks
    from tasks import init_app
    init_app(app)
    from tasks import fbit

    return app
