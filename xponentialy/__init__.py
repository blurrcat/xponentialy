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
    import admin
    return app
